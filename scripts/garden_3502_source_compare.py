#!/usr/bin/env python3
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from collections import defaultdict

GARDEN_SOURCES = [
    ("Hindi", "https://iptv-org.github.io/iptv/languages/hin.m3u"),
    ("Bhojpuri", "https://iptv-org.github.io/iptv/languages/bho.m3u"),
    ("English", "https://iptv-org.github.io/iptv/countries/in.m3u"),
    ("Sports", "https://iptv-org.github.io/iptv/countries/bd.m3u"),
    ("Music", "https://iptv-org.github.io/iptv/categories/music.m3u"),
    ("Cartoon", "https://iptv-org.github.io/iptv/categories/animation.m3u"),
    ("Science", "https://iptv-org.github.io/iptv/categories/documentary.m3u"),
    ("Sports", "https://iptv-org.github.io/iptv/categories/sports.m3u"),
    ("Sports", "https://iptv-org.github.io/iptv/countries/uk.m3u"),
    ("Sports", "https://iptv-org.github.io/iptv/countries/us.m3u"),
    ("Sports", "https://iptv-org.github.io/iptv/countries/nz.m3u"),
    ("Sports", "https://iptv-org.github.io/iptv/countries/za.m3u"),
    ("Sports", "https://iptv-org.github.io/iptv/countries/au.m3u"),
]
IPTV_ORG_INDEX = "https://iptv-org.github.io/iptv/index.m3u"
TIMEOUT = 12

BLOCK = ['tamil','telugu','malayalam','kannada','bengali','bangla','marathi','gujarati','punjabi','odia','oriya','assamese','urdu','sun tv','sun news','ktv','adithya','gemini','eenadu','etv telugu','asianet','manorama','flowers tv','mathrubhumi','mazhavil','surya tv','udaya','colors kannada','colors tamil','colors marathi','zee kannada','zee tamil','zee telugu','zee keralam','star suvarna','star vijay','star maa','jaya tv','polimer','puthiya','thanthi','abn andhra','tv9 telugu','tv9 kannada','tv9 marathi','news18 tamil','news18 kerala','news18 kannada','news18 assam','dd chandana','dd yadagiri','dd malayalam','dd podhigai','dd sahyadri','chithiram','jaya max']
ENG_HINTS = ['wion','ndtv','republic','times now','cnn-news18','cnn news18','india today','mirror now','newsx','dd india','cnbc','et now','bloomberg','bbc','al jazeera','dw english','france 24','discovery','history tv','travelxp','good times']
SPORT_HINTS = ['star sports','sony six','sony ten','sony espn','dd sports','willow','cricket','ptv sports','ten cricket','sports18','jio cricket','t sports','tsports','unite8 sports','unite sports','fox sports','1sports','ssc sports','astro cricket','sky sports cricket','super sport cricket','a sports','geo super']
INTL_SPORT = ['cricket','willow','fox cricket','sky sports cricket','tnt sport','tnt sports','super sport','supersport','star sports','sony six','sony ten','sony espn','t sports','tsports','dd sports','ptv sports','ten cricket','sports18','cricket gold','astro cricket','nine cricket','7 cricket','fox sports']


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode('utf-8', 'ignore')


def clean_name(name):
    name = re.sub(r'\s*\(\d{3,4}p\)\s*$', '', name, flags=re.I)
    name = re.sub(r'\s*\[.*?\]\s*$', '', name)
    return name.strip()


def parse(text, lang):
    out=[]; cur=None
    for line in text.splitlines():
        line=line.strip()
        if line.startswith('#EXTINF:'):
            name=line.split(',',1)[-1].strip() if ',' in line else ''
            group='General'
            m=re.search(r'group-title="([^"]*)"', line)
            if m: group=m.group(1).strip()
            cur=(clean_name(name), group)
        elif cur and line and not line.startswith('#') and line.startswith(('http://','https://')):
            out.append({'name':cur[0], 'group':cur[1], 'lang':lang, 'url':line})
            cur=None
    return [x for x in out if x['name'] and x['url']]


def cat(group, name):
    g=(group+' '+name).lower()
    if re.search(r'sport|cricket|football|hockey|tennis|wwe|boxing|soccer|t sports|star sports|sony six|sony ten|sony espn',g): return 'Sports'
    if re.search(r'news|wion|ndtv|republic|times now|bbc|cnn|aaj tak',g): return 'News'
    if re.search(r'movie|cinema|cineplex|film|classic',g): return 'Movie'
    if re.search(r'music|sangeet|mtv|9xm|song',g): return 'Music'
    if re.search(r'kid|cartoon|nick|pogo|hungama|disney|sony yay|cartoon network|discovery kids',g): return 'Cartoon'
    if re.search(r'lifestyle|fox life|tlc|travelxp|food|ndt v good times|good times|fashion|ftv',g): return 'Lifestyle'
    if re.search(r'science|discovery|national geographic|nat geo|animal planet|history tv|ngc',g): return 'Science'
    if re.search(r'relig|devot|bhakti|sanskar',g): return 'Devotional'
    if re.search(r'business|cnbc|et now|bloomberg',g): return 'Business'
    return 'Entertainment'


def blocked(name):
    n=name.lower(); return any(x in n for x in BLOCK)


def wanted(records):
    out=[]
    for ch in records:
        if blocked(ch['name']): continue
        n=ch['name'].lower()
        if ch['lang'] in ('Hindi','Bhojpuri'):
            out.append(ch); continue
        if ch['lang']=='English':
            if any(x in n for x in ENG_HINTS) or any(x in n for x in SPORT_HINTS):
                out.append(ch); continue
            if any(x in n for x in ['kid','cartoon','nick','pogo','hungama','disney','sony yay','cartoon network','discovery kids','music','mtv','9xm','9x ','b4u music','mastiii','masti','vh1','discovery','national geographic','nat geo','animal planet','history tv','fashion tv','ftv','fox life','tlc','travelxp']):
                out.append(ch); continue
        if ch['lang']=='Sports' and any(x in n for x in INTL_SPORT):
            out.append(ch)
    return out


def norm_name(s):
    return re.sub(r'\s+', ' ', s.strip().lower())


def parse_index(text):
    return parse(text, 'Source')


def check(url):
    try:
        req=urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0','Range':'bytes=0-8191'})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            body=r.read(8192)
            ok=200 <= getattr(r,'status',200) < 400 and bool(body)
            if ok and '.m3u8' in url.lower(): ok=b'#EXTM3U' in body
            return 'Working' if ok else 'Non-working'
    except Exception:
        return 'Non-working'


def main():
    print('[1/4] Downloading Garden actual source feeds...')
    records=[]
    seen=set()
    for lang,url in GARDEN_SOURCES:
        try: rows=parse(fetch(url), lang)
        except Exception as e:
            print('SOURCE ERROR',url,e); continue
        for r in rows:
            key=(r['name'],r['url'])
            if key not in seen:
                seen.add(key); r['category']=cat(r['group'],r['name']); records.append(r)
    records=wanted(records)

    print('[2/4] Downloading 3502 actual source...')
    index=parse_index(fetch(IPTV_ORG_INDEX))
    by_url={x['url']:x for x in index}
    by_name=defaultdict(list)
    for x in index: by_name[norm_name(x['name'])].append(x)

    print('[3/4] Comparing exact stream URLs...')
    rows=[]
    for g in records:
        same=by_url.get(g['url'])
        if same:
            relation='Same'
            matches=[same]
        else:
            matches=by_name.get(norm_name(g['name']),[])
            relation='Different URL' if matches else 'Not Found'
        rows.append((g,matches,relation))

    print('[4/4] Checking Garden source streams...')
    urls=list({g['url'] for g,_,_ in rows})
    status={}
    with ThreadPoolExecutor(max_workers=24) as ex:
        fut={ex.submit(check,u):u for u in urls}
        for f in as_completed(fut): status[fut[f]]=f.result()

    out=Path('garden_3502_source_comparison.md')
    lines=['# Garden vs 3502 — Actual Source Comparison','',f'- Garden actual source entries after Garden filters: **{len(rows)}**',f'- 3502 actual source: **{IPTV_ORG_INDEX}**','- Matching rule: **exact stream URL**','- Different/Not Found rule: channel name is used only after exact URL is absent.','']
    counts=defaultdict(int)
    for g,matches,rel in rows: counts[rel]+=1
    lines += [f'- Same: **{counts["Same"]}**',f'- Different URL: **{counts["Different URL"]}**',f'- Not Found: **{counts["Not Found"]}**','']
    for category in sorted(set(g['category'] for g,_,_ in rows)):
        lines += [f'## {category}','', '| Status | Match | Channel | Garden URL | 3502 URL |','|---|---|---|---|---|']
        for g,matches,rel in rows:
            if g['category']!=category: continue
            gs=status.get(g['url'],'Non-working')
            if not matches:
                lines.append(f'| {gs} | {rel} | {g["name"]} | {g["url"]} | — |')
            else:
                for m in matches:
                    lines.append(f'| {gs} | {rel} | {g["name"]} | {g["url"]} | {m["url"]} |')
        lines.append('')
    out.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f'Wrote {out} ({len(rows)} Garden entries)')

if __name__=='__main__': main()
