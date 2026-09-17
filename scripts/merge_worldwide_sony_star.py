#!/usr/bin/env python3
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

WORLDWIDE_URL = 'https://iptv-org.github.io/iptv/streams/in.m3u'
WORKING = 'playlist_working.m3u'
NONWORKING = 'playlist_nonworking.m3u'
TIMEOUT = 8

CATEGORY_ORDER = {
    'News': 0, 'Movies': 1, 'Music': 2, 'Sports': 3,
    'Entertainment': 4, 'Lifestyle': 5, 'Infotainment': 6,
    'Science': 7, 'Kids': 8, 'Business': 9, 'Doordarshan': 10,
    'Non Jio': 11
}

PATTERNS = [
    r'\bSony Entertainment Television\b', r'\bSony SAB\b', r'\bSony Pal\b',
    r'\bSony Max(?: 2)?\b', r'\bSony Wah\b', r'\bSony Pix\b',
    r'\bSony Sports Ten [1-5]\b', r'\bSony Marathi\b', r'\bSony Aath\b',
    r'\bSony YAY!?\b', r'\bSony BBC Earth\b',
    r'\bStar ?Plus\b', r'\bStar Bharat\b', r'\bStar Jalsha\b',
    r'\bStar Pravah\b', r'\bStar Vijay\b', r'\bStar Maa\b',
    r'\bStar Suvarna\b', r'\bStar Utsav(?: Movies)?\b',
    r'\bStar Gold(?: 2| Romance| Thrills| Select)?\b',
    r'\bStar Sports(?: [1-3])?(?: Hindi)?\b',
    r'\bStar Sports Select [1-2]\b', r'\bStar Sports Khel\b'
]
RX = re.compile('(?:' + '|'.join(PATTERNS) + ')', re.I)

MANUAL = [
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
            hls = '.m3u8' in url.lower() or '#EXTM3U' in t or 'mpegurl' in r.headers.get('Content-Type', '').lower()
            return '#EXTM3U' in t if hls else True
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

    # Explicit requested worldwide/UK entries. Only add if the exact URL is not already present.
    for m in MANUAL:
        url = clean(m['url'])
        if not url or url in known or url in seen:
            continue
        seen.add(url)
        candidates.append({
            'extinf': f'#EXTINF:-1 tvg-name="{m["name"]}" tvg-logo="{m["logo"]}" group-title="{m["category"]}",{m["name"]}',
            'extra': [],
            'url': url,
            'name': m['name'],
            'category': m['category']
        })

    if not candidates:
        print('WORLDWIDE SONY/STAR + MANUAL: no new stream URLs')
        return

    working = []
    nonworking = []
    for e in candidates:
        (working if check(e['url']) else nonworking).append(e)

    append_entries(WORKING, working)
    append_entries(NONWORKING, nonworking)
    print('WORLDWIDE SONY/STAR + MANUAL NEW:', len(candidates))
    print('  WORKING:', len(working))
    print('  NON-WORKING:', len(nonworking))
    for group in ('Movies', 'Sports', 'Entertainment'):
        print(' ', group, sum(1 for x in candidates if x['category'] == group))
    for e in candidates:
        if e['name'] in {'Utsav Bharat [UK]', 'Utsav Plus [UK]', 'Cricket Gold'}:
            print(' ', e['name'], '=>', 'WORKING' if e in working else 'NON-WORKING')


if __name__ == '__main__':
    main()
