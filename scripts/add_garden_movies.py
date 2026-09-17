from pathlib import Path
from urllib.request import urlopen

GARDEN_URL = "https://raw.githubusercontent.com/Sri014/Garden/main/working.m3u"
WORKING = Path("playlist_working.m3u")
NONWORKING = Path("playlist_nonworking.m3u")


def urls(text):
    return {line.strip() for line in text.splitlines() if line.strip().startswith(("http://", "https://"))}


def parse_movies(text):
    lines = text.splitlines()
    out = []
    extinf = None
    for line in lines:
        line = line.rstrip("\r")
        if line.startswith("#EXTINF:"):
            extinf = line
        elif extinf and line.startswith(("http://", "https://")):
            if 'group-title="Movies"' in extinf:
                out.append((extinf, line.strip()))
            extinf = None
        elif line.strip() and not line.startswith("#"):
            extinf = None
    return out


def main():
    garden = urlopen(GARDEN_URL, timeout=30).read().decode("utf-8", "ignore")
    working_text = WORKING.read_text(errors="ignore") if WORKING.exists() else "#EXTM3U\n"
    nonworking_text = NONWORKING.read_text(errors="ignore") if NONWORKING.exists() else ""

    existing = urls(working_text) | urls(nonworking_text)
    movies = parse_movies(garden)
    additions = [(meta, url) for meta, url in movies if url not in existing]

    if additions:
        with WORKING.open("a", encoding="utf-8") as f:
            if not working_text.endswith("\n"):
                f.write("\n")
            for meta, url in additions:
                f.write(meta + "\n" + url + "\n")

    print(f"Garden Movies found: {len(movies)}")
    print(f"New movie streams added to working: {len(additions)}")
    for meta, url in additions:
        name = meta.split(",", 1)[-1].strip() if "," in meta else "Unknown"
        print(f"ADD: {name} -> {url}")


if __name__ == "__main__":
    main()
