#!/usr/bin/env python3
import re
from urllib.request import Request, urlopen

GARDEN_URL = 'https://raw.githubusercontent.com/Sri014/Garden/main/working.m3u'
WORKING = 'playlist_working.m3u'
NONWORKING = 'playlist_nonworking.m3u'
TIMEOUT = 8


def fetch(url, timeout=45):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 IPTV Playlist Generator'})
    with urlopen(req, timeout=timeout) as r:
        return r.read().decode('utf-8', errors='replace')


def parse_m3u(text):
    out = []
    current = None
    for raw in text.splitlines():
        line = raw.strip('\ufeff\r')
        if line.startswith('#EXTINF:'):
            current = {'extinf': line, 'extra': [], 'url': ''}
        elif current is not None and line.startswith('#'):
            current['extra'].append(line)
        elif current is not None and line.startswith(('http://', 'https://')):
            current['url'] = line.strip()
            out.append(current)
            current = None
    return out


def urls(path):
    try:
        return {e['url'] for e in parse_m3u(open(path, encoding='utf-8').read()) if e['url']}
    except FileNotFoundError:
        return set()


def is_movies(e):
    ext = e['extinf']
    m = re.search(r'group-title="([^"]*)"', ext, re.I)
    if m and m.group(1).strip().lower() == 'movies':
        return True
    name = ext.split(',', 1)[-1].strip().lower()
    return any(x in name for x in ('movie', 'cinema', 'goldmines', 'sony max', 'sony wah', 'b4u ', 'epic bhojpuri', 'manoranjan grand', 'manoranjan prime', 'mbc bollywood', 'mh one movies', 'pocket films', 'shemaroo josh', 'shubh cinema', 'south station', 'star gold', '&xplor'))


def check(url):
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': '*/*'})
        with urlopen(req, timeout=TIMEOUT) as r:
            if r.status not in (200, 206):
                return False
            b = r.read(8192)
            if not b:
                return False
            if '.m3u8' in url.lower() or 'mpegurl' in r.headers.get('Content-Type', '').lower():
                return b'#EXTM3U' in b
            return True
    except Exception:
        return False


def append(path, entries):
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
        garden = parse_m3u(fetch(GARDEN_URL))
    except Exception as e:
        print('GARDEN FETCH ERROR:', e)
        return

    known = urls(WORKING) | urls(NONWORKING)
    candidates = []
    seen = set()

    for e in garden:
        if not is_movies(e):
            continue
        url = e['url'].strip()
        if not url or url in known or url in seen:
            continue
        seen.add(url)
        ext = e['extinf']
        if 'group-title=' in ext:
            ext = re.sub(r'group-title="[^"]*"', 'group-title="Movies"', ext, count=1)
        candidates.append({'extinf': ext, 'extra': e['extra'], 'url': url, 'name': ext.split(',', 1)[-1].strip()})

    working, nonworking = [], []
    for e in candidates:
        (working if check(e['url']) else nonworking).append(e)

    append(WORKING, working)
    append(NONWORKING, nonworking)
    print('GARDEN MOVIES NEW:', len(candidates), 'WORKING:', len(working), 'NONWORKING:', len(nonworking))
    for e in candidates:
        print(e['name'], '=>', 'WORKING' if e in working else 'NONWORKING', '=>', e['url'])


if __name__ == '__main__':
    main()
