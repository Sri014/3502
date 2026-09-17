#!/usr/bin/env python3
from pathlib import Path
import re

SRC = Path('playlist_working.m3u')
OUT = Path('playlists/sony-star-india.m3u')

# Explicit Indian Sony / Star channel names only.
# Generic "Sony" or "Star" matching is intentionally avoided so foreign channels are excluded.
PATTERNS = [
    r'^Sony Entertainment Television(?: HD)?(?: \(.*\))?$',
    r'^Sony SAB(?: HD)?(?: \(.*\))?$',
    r'^Sony Pal(?: HD)?(?: \(.*\))?$',
    r'^Sony MAX(?: 2)?(?: HD)?(?: \(.*\))?$',
    r'^Sony Max(?: 2)?(?: HD)?(?: \(.*\))?$',
    r'^Sony Pix(?: HD)?(?: \(.*\))?$',
    r'^Sony Wah(?: HD)?(?: \(.*\))?$',
    r'^Sony Sports Ten [1-5](?: HD)?(?: \(.*\))?$',
    r'^Sony Marathi(?: HD)?(?: \(.*\))?$',
    r'^Sony Aath(?: HD)?(?: \(.*\))?$',
    r'^Sony YAY!?(?: HD)?(?: \(.*\))?$',
    r'^Sony BBC Earth(?: HD)?(?: \(.*\))?$',
    r'^Star Plus(?: HD)?(?: \(.*\))?$',
    r'^StarPlus(?: HD)?(?: \(.*\))?$',
    r'^Star Bharat(?: HD)?(?: \(.*\))?$',
    r'^Star Jalsha(?: HD)?(?: \(.*\))?$',
    r'^Star Pravah(?: HD)?(?: \(.*\))?$',
    r'^Star Vijay(?: HD)?(?: \(.*\))?$',
    r'^Star Maa(?: HD)?(?: \(.*\))?$',
    r'^Star Suvarna(?: HD)?(?: \(.*\))?$',
    r'^Star Utsav(?: HD)?(?: \(.*\))?$',
    r'^Star Utsav Movies(?: HD)?(?: \(.*\))?$',
    r'^Star Gold(?: HD)?(?: 2| Romance| Thrills| Select)?(?: HD)?(?: \(.*\))?$',
    r'^Star Sports(?: [1-9])?(?: HD)?(?: Select [12])?(?: Hindi)?(?: \(.*\))?$',
    r'^Star Sports Khel(?: HD)?(?: \(.*\))?$',
]
REGEX = [re.compile(x, re.I) for x in PATTERNS]

def main():
    if not SRC.exists():
        raise SystemExit('Missing playlist_working.m3u')
    lines = SRC.read_text(encoding='utf-8', errors='ignore').splitlines()
    selected = []
    i = 0
    while i < len(lines):
        if lines[i].startswith('#EXTINF:'):
            name = lines[i].split(',', 1)[1].strip() if ',' in lines[i] else ''
            block = [lines[i]]
            i += 1
            while i < len(lines) and not lines[i].startswith('#EXTINF:'):
                block.append(lines[i])
                i += 1
            if any(rx.search(name) for rx in REGEX):
                selected.extend(block)
        else:
            i += 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text('#EXTM3U\n' + '\n'.join(selected) + ('\n' if selected else ''), encoding='utf-8')
    print(f'Sony/Star India working channels: {sum(1 for x in selected if x.startswith("#EXTINF:") )}')

if __name__ == '__main__':
    main()
