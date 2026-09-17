#!/usr/bin/env python3
import json
import re
import urllib.request
from pathlib import Path

GARDEN_WORKING = 'https://raw.githubusercontent.com/Sri014/Garden/main/working.m3u'
GARDEN_NONWORKING = 'https://raw.githubusercontent.com/Sri014/Garden/main/non_working.m3u'
W = Path('playlist_working.m3u')
N = Path('playlist_nonworking.m3u')
R = Path('cross_sync.json')


def norm_name(s):
    s = s.lower().strip()
    s = re.sub(r'\s*\[[^\]]+\]\s*$', '', s)
    s = re.sub(r'\s*\(?\s*(?:hd|sd|fhd|uhd|\d{3,4}p)\s*\)?\s*$', '', s)
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()


def parse(text):
    lines = text.replace('\r', '').splitlines()
    rows = []
    i = 0
    while i < len(lines):
        if lines[i].startswith('#EXTINF:'):
            info = lines[i]
            url = lines[i + 1].strip() if i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].startswith('#') else ''
            name = info.rsplit(',', 1)[-1].strip() if ',' in info else ''
            if url:
                rows.append((info, url, name))
            i += 2
        else:
            i += 1
    return rows


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode('utf-8', 'replace')


def render(rows):
    return '#EXTM3U\n' + ''.join(f'{info}\n{url}\n' for info, url, _ in rows)


working = parse(W.read_text(encoding='utf-8', errors='ignore') if W.exists() else '#EXTM3U\n')
nonworking = parse(N.read_text(encoding='utf-8', errors='ignore') if N.exists() else '#EXTM3U\n')

garden_w = parse(fetch(GARDEN_WORKING))
garden_n = parse(fetch(GARDEN_NONWORKING))

# URL is the primary comparison key. Channel name is used only to classify
# an unmatched Garden URL as Different URL vs Not Found.
working_urls = {url.strip() for _, url, _ in working if url.strip()}
nonworking_urls = {url.strip() for _, url, _ in nonworking if url.strip()}
all_3502_names = {}
for info, url, name in working + nonworking:
    key = norm_name(name)
    if key:
        all_3502_names.setdefault(key, []).append(url.strip())

same_working = []
same_nonworking = []
different_working = []
different_nonworking = []
notfound_working = []
notfound_nonworking = []

for status, rows in [('working', garden_w), ('nonworking', garden_n)]:
    for info, url, name in rows:
        url = url.strip()
        key = norm_name(name)
        if url in working_urls:
            same_working.append((info, url, name))
        elif url in nonworking_urls:
            same_nonworking.append((info, url, name))
        elif key in all_3502_names:
            (different_working if status == 'working' else different_nonworking).append((info, url, name))
        else:
            (notfound_working if status == 'working' else notfound_nonworking).append((info, url, name))

# Add every Garden URL that is not already present in either 3502 playlist.
# Garden working -> 3502 working; Garden non-working -> 3502 non-working.
add_working = different_working + notfound_working
add_nonworking = different_nonworking + notfound_nonworking

for row in add_working:
    if row[1] not in working_urls and row[1] not in nonworking_urls:
        working.append(row)
        working_urls.add(row[1])
for row in add_nonworking:
    if row[1] not in working_urls and row[1] not in nonworking_urls:
        nonworking.append(row)
        nonworking_urls.add(row[1])

W.write_text(render(working), encoding='utf-8')
N.write_text(render(nonworking), encoding='utf-8')

report = {
    'sources': {'garden_working': GARDEN_WORKING, 'garden_nonworking': GARDEN_NONWORKING},
    'rule': 'Exact stream URL match first; channel name only distinguishes Different URL from Not Found.',
    'garden_working': len(garden_w),
    'garden_nonworking': len(garden_n),
    'same_url_working': len(same_working),
    'same_url_nonworking': len(same_nonworking),
    'different_url_working': len(different_working),
    'different_url_nonworking': len(different_nonworking),
    'not_found_working': len(notfound_working),
    'not_found_nonworking': len(notfound_nonworking),
    'added_to_working': len(add_working),
    'added_to_nonworking': len(add_nonworking),
    'added_working_channels': [{'name': x[2], 'url': x[1]} for x in add_working],
    'added_nonworking_channels': [{'name': x[2], 'url': x[1]} for x in add_nonworking],
}
R.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')

print('Garden vs 3502 exact URL sync complete')
for k, v in report.items():
    if isinstance(v, int):
        print(f'{k}: {v}')
