#!/usr/bin/env python3
import re
from urllib.request import Request, urlopen

WORLDWIDE_URL = 'https://iptv-org.github.io/iptv/streams/in.m3u'
WORKING = 'playlist_working.m3u'
NONWORKING = 'playlist_nonworking.m3u'
TIMEOUT = 8

PATTERNS = [
    r'\bSony Sports Ten [1-5]\b',
    r'\bStar Sports(?: [1-3])?(?: Hindi)?\b',
    r'\bStar Sports Select [1-2]\b',
    r'\bStar Sports Khel\b'
]
RX = re.compile('(?:' + '|'.join(PATTERNS) + ')', re.I)

# Explicit worldwide streams requested by user. They are checked and then
# placed into playlist_working.m3u or playlist_nonworking.m3u accordingly.
MANUAL = [
    {
        'name': 'Sony Sports Ten 1 HD',
        'url': 'https://cloudplay-sonyliv.pages.dev/ten1hd.m3u8',
        'logo': 'https://xstreamcp-assets-msp.streamready.in/assets/LIVETV/LIVECHANNEL/LIVETV_LIVETVCHANNEL_SONY_SPORTS_TEN_1/images/LOGO_HD/image.png',
        'category': 'Sports'
    },
    {
        'name': 'Sony Sports Ten 4',
        'url': 'https://cloudplay-sonyliv.pages.dev/ten4.m3u8',
        'logo': 'https://dtil.tmsimg.com/assets/GNLZZGG0025T4PV.png?lock=720x540',
        'category': 'Sports'
    },
    {
        'name': 'Sony Sports Ten 4 Telugu',
        'url': 'https://cloudplay-sonyliv.pages.dev/ten4hd.m3u8',
        'logo': 'https://xstreamcp-assets-msp.streamready.in/assets/LIVETV/LIVECHANNEL/LIVETV_LIVETVCHANNEL_SONY_SPORTS_TEN_4/images/LOGO_HD/image.png',
        'category': 'Sports'
    },
    {
        'name': 'Sony Sports Ten 5',
        'url': 'https://cloudplay-sonyliv.pages.dev/ten5.m3u8',
        'logo': 'https://xstreamcp-assets-msp.streamready.in/assets/LIVETV/LIVECHANNEL/LIVETV_LIVETVCHANNEL_SONY_SPORTS_TEN_5/images/LOGO_HD/image.png',
        'category': 'Sports'
    },
    {
        'name': 'Sony Sports Ten 5 HD',
        'url': 'https://cloudplay-sonyliv.pages.dev/ten5hd.m3u8',
        'logo': 'https://xstreamcp-assets-msp.streamready.in/assets/LIVETV/LIVECHANNEL/LIVETV_LIVETVCHANNEL_SONY_SPORTS_TEN_5/images/LOGO_HD/image.png',
        'category': 'Sports'
    },
    {
        'name': 'Star Sports 1 Hindi',
        'url': 'http://103.253.18.58:8000/play/a03o',
        'logo': 'https://i.imgur.com/FtRT73R.png',
        'category': 'Sports'
    },
    {
        'name': 'Star Sports 2 HD',
        'url': 'http://tvsen5.aynascope.net/cXPB2LKkErN9/index.m3u8',
        'logo': 'https://i.imgur.com/FtRT73R.png',
        'category': 'Sports'
    },
    {
        'name': 'Star Sports 2 Hindi HD',
        'url': 'http://103.157.248.140:8000/play/a01m/index.m3u8',
        'logo': 'https://i.imgur.com/FtRT73R.png',
        'category': 'Sports'
    },
    {
        'name': 'Star Sports Khel',
        'url': 'http://103.175.73.12:8080/live/151/151_0.m3u8',
        'logo': 'https://i.imgur.com/FtRT73R.png',
        'category': 'Sports'
    },
    {
        'name': 'Utsav Bharat [UK]',
        'url': 'http://xown.site/token/stream.php?id=1484530&token=jzVQIX8Sa8Du818wRZdAH2eDDBHwGaqq',
        'logo': 'http://103.176.90.118/picons/logos/logos/UTSAV-BHARAT.png',
        'category': 'Entertainment'
    },
    {
        'name': 'Utsav Plus [UK]',
        'url': 'http://xown.site/token/stream.php?id=1484512&token=jzVQIX8Sa8Du818wRZdAH2eDDBHwGaqq',
        'logo': 'http://103.176.90.118/picons/logos/logos/UTSAV-PLUS.png',
        'category': 'Entertainment'
    },
    {
        'name': 'Cricket Gold',
        'url': 'https://streams2.sofast.tv/scheduler/scheduleMaster/418.m3u8',
        'logo': 'https://i.imgur.com/UvbHjlx.png',
        'category': 'Sports'
    }
]


def clean(s):
    return re.sub(r'\s+', ' ', str(s or '').strip())


def category(name):
    n = clean(name).lower()
    if any(x in n for x in ('star sports', 'sony sports', 'sports khel', 'cricket gold')):
        return 'Sports'
    if any(x in n for x in ('sony max', 'sony wah', 'sony pix', 'star gold', 'star utsav movies')):
        return 'Movies'
    if 'e24 music' in n:
        return 'Music'
    return 'Entertainment'


def fetch_text(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 IPTV Playlist Generator'})
    with urlopen(req, timeout=45) as r:
        return r.read().decode('utf-8', errors='replace')


def parse_m3u(text):
    lines = text.splitlines()
    out = []
    current = None
    for line in lines:
        line = line.strip('\ufeff\r')
        if line.startswith('#EXTINF:'):
            current = {'extinf': line, 'extra': [], 'url': ''}
        elif current is not None and line.startswith('#'):
            current['extra'].append(line)
        elif current is not None and line.startswith(('http://', 'https://')):
            current['url'] = line
            out.append(current)
            current = None
    return out


def existing_urls(path):
    try:
        return {x['url'] for x in parse_m3u(open(path, encoding='utf-8').read()) if x['url']}
    except FileNotFoundError:
        return set()


def check(url):
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': '*/*'})
        with urlopen(req, timeout=TIMEOUT) as r:
            if r.status not in (200, 206):
                return False
            b = r.read(8192)
            if not b:
                return False
            t = b.decode('utf-8', errors='ignore')
            if '.m3u8' in url.lower() or '#EXTM3U' in t or 'mpegurl' in r.headers.get('Content-Type', '').lower():
                return '#EXTM3U' in t
            return True
    except Exception:
        return False


def append_entries(path, entries):
    if not entries:
        return
    try:
        text = open(path, encoding='utf-8').read().rstrip() + '\n'
    except FileNotFoundError:
        text = '#EXTM3U\n'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
        for e in entries:
            f.write(e['extinf'] + '\n')
            for x in e['extra']:
                f.write(x + '\n')
            f.write(e['url'] + '\n')


def main():
    try:
        world = parse_m3u(fetch_text(WORLDWIDE_URL))
    except Exception as e:
        print('WORLDWIDE FETCH ERROR:', e)
        world = []

    known = existing_urls(WORKING) | existing_urls(NONWORKING)
    candidates = []
    seen = set()

    for e in world:
        url = clean(e['url'])
        name = clean(e['extinf'].split(',', 1)[-1])
        if not url or url in known or url in seen or not RX.search(name):
            continue
        seen.add(url)
        group = category(name)
        ext = e['extinf']
        if 'group-title=' in ext:
            ext = re.sub(r'group-title="[^"]*"', 'group-title="' + group + '"', ext, count=1)
        else:
            ext = ext.replace(',', ' group-title="' + group + '",', 1)
        candidates.append({'extinf': ext, 'extra': e['extra'], 'url': url, 'name': name, 'category': group})

    # Explicit entries are considered even when the worldwide source changes its
    # display name. Exact URL de-duplication prevents duplicate stream URLs.
    for m in MANUAL:
        url = clean(m['url'])
        if not url or url in known or url in seen:
            continue
        seen.add(url)
        candidates.append({
            'extinf': f'#EXTINF:-1 tvg-name="{m["name"]}" tvg-logo="{m["logo"]}" group-title="{m["category"]}",{m["name"]}',
            'extra': [], 'url': url, 'name': m['name'], 'category': m['category']
        })

    working, nonworking = [], []
    for e in candidates:
        (working if check(e['url']) else nonworking).append(e)

    append_entries(WORKING, working)
    append_entries(NONWORKING, nonworking)
    print('NEW:', len(candidates), 'WORKING:', len(working), 'NONWORKING:', len(nonworking))
    for e in candidates:
        if e['name'] in {m['name'] for m in MANUAL}:
            print(e['name'], '=>', 'WORKING' if e in working else 'NONWORKING')


if __name__ == '__main__':
    main()
