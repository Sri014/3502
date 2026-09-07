#!/usr/bin/env python3
import json, re, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

CHANNELS_URL='https://iptv-org.github.io/api/channels.json'; FEEDS_URL='https://iptv-org.github.io/api/feeds.json'; STREAMS_URL='https://iptv-org.github.io/api/streams.json'
WORKING_OUTPUT='playlist_working.m3u'; NONWORKING_OUTPUT='playlist_nonworking.m3u'; WORKERS=24; TIMEOUT=8
HINDI={'hin','hindi'}; ENGLISH={'eng','english'}; BHOJPURI={'bho','bhojpuri'}
REGIONAL={'tam','tamil','tel','telugu','ben','bengali','mar','marathi','guj','gujarati','kan','kannada','mal','malayalam','pan','punjabi','ori','odia','oriya','asm','assamese','urd','urdu','kas','kashmiri','nep','nepali','kok','konkani','san','sanskrit','snd','sindhi','mai','maithili','doi','dogri','mni','manipuri'}
BAD_WORDS={'evidya','pmevidya','swayamprabha','vandegujarat','devotional','devotion','bhakti','bhajan','spiritual','prayer','worship','god tv','religious','religion','aastha','aastha bhajan','angel','adinath','anand','aryan','awakening','divya darshan','divya darshan24','darshan24'}
FOREIGN_COUNTRIES={'US':'USA - Hindi','GB':'UK - Hindi','AE':'Middle East - Hindi','QA':'Middle East - Hindi','SA':'Middle East - Hindi','BH':'Middle East - Hindi','KW':'Middle East - Hindi','OM':'Middle East - Hindi'}
CATEGORIES=('News','Movies','Music','Sports','Entertainment','Lifestyle','Infotainment','Science','Kids','Business','Doordarshan','Non Jio')

# JioTV Hindi category/name rules. Exact known channel names take priority over generic IPTV-org categories.
JIO_NAMES={
'News':{'aaj tak','abp news','india tv','ndtv india','ndtv 24x7','news18 india','news18 hindi','zee news','times now navbharat','republic bharat','tv9 bharatvarsh','news24','bharat express','good news today','firstpost','cnn-news18','cnn news18'},
'Movies':{'star gold','star gold hd','star gold 2','star gold 2 hd','star gold romance','star gold thrills','star gold select','star gold select hd','sony max','sony max hd','sony max 2','sony wah','zee cinema','zee cinema hd','zee bollywood','zee action','zee classic','zee anmol cinema','&pictures','&pictures hd','&xplor hd','colors cineplex','colors cineplex hd','colors cineplex superhits','colors cineplex bollywood','star utsav movies','b4u movies'},
'Music':{'mtv','9xm','9x music','9x jhakaas','zoom','music india','mastiii','b4u music','zing','mood mix','songsara','9x tashan','9x jalwa'},
'Sports':{'star sports 1','star sports 1 hd','star sports 2','star sports 2 hd','star sports 3','star sports 3 hd','star sports 1 hindi','star sports hindi 1','star sports khel','star sports khel hd','sony sports ten 1','sony sports ten 2','sony sports ten 3','sony sports ten 4','sony sports ten 5','sony sports ten 1 hd','sony sports ten 2 hd','sony sports ten 3 hd','sony sports ten 5 hd','sports18 1','sports18 1 hd','sports18 khel','wion sports'},
'Kids':{'nick','nick hd+','sonic','sonic hd','hungama','hungama hd','disney channel','disney junior','pogo','discovery kids','cartoon network','super hungama','marvel hq'},
'Infotainment':{'discovery','discovery hd world','history tv18','history tv18 hd','nat geo','nat geo hd','national geographic','national geographic hd','sony bbc earth','sony bbc earth hd','animal planet','animal planet hd','tlc','tata play fitness','epic','epic hd','travel xp','travel xp hd','food food','good times'},
'Lifestyle':{'food food','food food hd','travelxp','travel xp','tlc','fashion tv','fashion tv hd','living foodz','living foodz hd'},
'Business':{'cnbc tv18','cnbc tv18 prime','cnbc awaaz','zee business','et now','et now swadesh','bloomberg tv','business today'},
'Doordarshan':{'dd national','dd news','dd india','dd sports','dd kisan','dd bharati','dd urdu','doordarshan'},
'Entertainment':{'star plus','star plus hd','sony entertainment television','sony set hd','sony sab','sony sab hd','colors','colors hd','zee tv','zee tv hd','star bharat','star bharat hd','&tv','&tv hd','colors rishtey','sony pal','zee anmol','star utsav','dangal tv','dangal 2','big magic','shemaroo umang','shemaroo tv'}
}
KEYWORDS={'News':{'news','breaking','bulletin','politics','headlines'},'Movies':{'movie','movies','cinema','film','films'},'Music':{'music','songs','song','mtv','radio music'},'Sports':{'sport','sports','cricket','football','soccer','tennis','golf','racing','wrestling'},'Lifestyle':{'lifestyle','food','travel','fashion','home','cooking','cookery'},'Science':{'science','technology','tech','space','nature'},'Kids':{'kids','children','child','cartoon','animation','junior'},'Infotainment':{'documentary','education','history','knowledge','discovery','learning'},'Entertainment':{'entertainment','comedy','drama','reality','serial','show'}}

def clean(v): return re.sub(r'\s+',' ',str(v or '').strip())
def norm(v):
    if isinstance(v,list): return ' '.join(norm(x) for x in v)
    if isinstance(v,dict): return ' '.join(norm(x) for x in v.values())
    return clean(v).lower()
def fetch_json(url):
    r=Request(url,headers={'User-Agent':'Mozilla/5.0 IPTV Playlist Generator'})
    with urlopen(r,timeout=45) as x:return json.loads(x.read().decode('utf-8',errors='replace'))
def get_languages(feed): return {norm(x) for x in feed.get('languages',[]) if norm(x)}
def exact_jio_category(name,channel):
    n=norm(name); n=re.sub(r'\s+\d+$','',n)
    for cat,names in JIO_NAMES.items():
        if n in names:return cat
    return None
def get_category(channel):
    name=clean(channel.get('name','')); exact=exact_jio_category(name,channel)
    if exact:return exact
    # Preserve only JioTV-style category when IPTV-org category is directly usable.
    for value in channel.get('categories',[]):
        v=norm(value)
        mapping={'news':'News','movies':'Movies','movie':'Movies','music':'Music','sports':'Sports','entertainment':'Entertainment','lifestyle':'Lifestyle','infotainment':'Infotainment','science':'Science','kids':'Kids','children':'Kids','animation':'Kids','documentary':'Infotainment','education':'Infotainment','business':'Business','business news':'Business','finance':'Business','doordarshan':'Doordarshan','dd':'Doordarshan'}
        if v in mapping:return mapping[v]
    text=norm([channel.get('name',''),channel.get('network',''),channel.get('alt_names',[])])
    if any(k in text for k in JIO_NAMES['Doordarshan']):return 'Doordarshan'
    if any(k in text for k in JIO_NAMES['Business']):return 'Business'
    for cat in ('News','Movies','Music','Sports','Lifestyle','Infotainment','Science','Kids','Entertainment'):
        if any(k in text for k in KEYWORDS[cat]):return cat
    return 'Non Jio'
def is_bad(channel,feed):
    text=norm([channel.get('id',''),channel.get('name',''),channel.get('network',''),channel.get('alt_names',[]),feed.get('id',''),feed.get('name',''),feed.get('alt_names',[])])
    return any(w in text for w in BAD_WORDS)
def get_stream_feed(stream,feeds):
    sf=stream.get('feed')
    if sf:
        for f in feeds:
            if str(f.get('id',''))==str(sf):return f
    for f in feeds:
        if f.get('is_main'):return f
    return feeds[0] if feeds else {}
def get_region_group(channel,feed):
    c=clean(channel.get('country','')).upper(); langs=get_languages(feed)
    if c=='IN':
        if langs&REGIONAL:return None
        if langs&HINDI:return 'India - Hindi'
        if langs&ENGLISH:return 'India - English'
        if langs&BHOJPURI:return 'India - Bhojpuri'
        return None
    if c in FOREIGN_COUNTRIES and langs&HINDI:return FOREIGN_COUNTRIES[c]
    return None
def build_candidates(channels,feeds,streams):
    fi={}
    for f in feeds:
        if f.get('channel'):fi.setdefault(f['channel'],[]).append(f)
    si={}
    for s in streams:
        cid=s.get('channel'); u=clean(s.get('url',''))
        if cid and u.startswith(('http://','https://')):si.setdefault(cid,[]).append(s)
    out={}
    for ch in channels:
        cid=ch.get('id')
        if not cid:continue
        fs=fi.get(cid,[])
        for s in si.get(cid,[]):
            u=clean(s.get('url',''))
            if not u or u in out:continue
            f=get_stream_feed(s,fs)
            if is_bad(ch,f):continue
            rg=get_region_group(ch,f)
            if rg is None:continue
            out[u]={'channel':ch,'feed':f,'stream':s,'url':u,'region_group':rg,'name':clean(ch.get('name',cid)),'category':get_category(ch)}
    return out
def headers(s):
    h={'User-Agent':s.get('user_agent') or 'Mozilla/5.0','Accept':'*/*'}
    if s.get('referrer'):h['Referer']=s['referrer']
    return h
def check_stream(i):
    try:
        with urlopen(Request(i['url'],headers=headers(i['stream'])),timeout=TIMEOUT) as r:
            if r.status not in (200,206):return False
            b=r.read(8192)
            if not b:return False
            t=b.decode('utf-8',errors='ignore'); hls='.m3u8' in i['url'].lower() or '#EXTM3U' in t or 'mpegurl' in r.headers.get('Content-Type','').lower()
            return '#EXTM3U' in t if hls else True
    except Exception:return False
def sort_items(items):
    order={n:i for i,n in enumerate(CATEGORIES)};return sorted(items,key=lambda x:(order[x['category']],x['name'].lower(),x['url']))
def write_playlist(items,path):
    counters={}
    with open(path,'w',encoding='utf-8') as p:
        p.write('#EXTM3U\n')
        for i in sort_items(items):
            key=(i['category'],i['name'].lower());counters[key]=counters.get(key,0)+1;n=counters[key];dn=i['name'] if n==1 else f"{i['name']} {n}"
            ch=i['channel'];p.write(f'#EXTINF:-1 tvg-id="{clean(ch.get("id",""))}" tvg-name="{dn}" tvg-logo="{clean(ch.get("logo",""))}" group-title="{i["category"]}",{dn}\n')
            if i['stream'].get('referrer'):p.write(f"#EXTVLCOPT:http-referrer={i['stream']['referrer']}\n")
            if i['stream'].get('user_agent'):p.write(f"#EXTVLCOPT:http-user-agent={i['stream']['user_agent']}\n")
            p.write(i['url']+'\n')
def main():
    try: ch=fetch_json(CHANNELS_URL);fe=fetch_json(FEEDS_URL);st=fetch_json(STREAMS_URL)
    except Exception as e:print('ERROR:',e);sys.exit(1)
    items=list(build_candidates(ch,fe,st).values());print(f'Selected unique streams: {len(items)}')
    working=[];non=[]
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        jobs={ex.submit(check_stream,i):i for i in items}
        for f in as_completed(jobs):(working if f.result() else non).append(jobs[f])
    write_playlist(working,WORKING_OUTPUT);write_playlist(non,NONWORKING_OUTPUT)
    for title,arr in [('WORKING',working),('NON-WORKING',non)]:
        print(title,len(arr));
        for c in CATEGORIES: 
            n=sum(1 for x in arr if x['category']==c)
            if n:print(' ',c,n)
if __name__=='__main__':main()
