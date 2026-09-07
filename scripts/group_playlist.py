#!/usr/bin/env python3

import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

CHANNELS_URL = "https://iptv-org.github.io/api/channels.json"
FEEDS_URL = "https://iptv-org.github.io/api/feeds.json"
STREAMS_URL = "https://iptv-org.github.io/api/streams.json"

WORKING_OUTPUT = "playlist_working.m3u"
NONWORKING_OUTPUT = "playlist_nonworking.m3u"
WORKERS = 24
TIMEOUT = 8

HINDI = {"hin", "hindi"}
ENGLISH = {"eng", "english"}
BHOJPURI = {"bho", "bhojpuri"}

# Explicitly excluded Indian regional languages.
REGIONAL = {
    "tam", "tamil", "tel", "telugu", "ben", "bengali",
    "mar", "marathi", "guj", "gujarati", "kan", "kannada",
    "mal", "malayalam", "pan", "punjabi", "ori", "odia", "oriya",
    "asm", "assamese", "urd", "urdu", "kas", "kashmiri",
    "nep", "nepali", "kok", "konkani", "san", "sanskrit",
    "snd", "sindhi", "mai", "maithili", "doi", "dogri", "mni", "manipuri",
}

BAD_WORDS = {"evidya", "pmevidya", "swayamprabha", "vandegujarat"}

# Canada intentionally excluded.
FOREIGN_COUNTRIES = {
    "US": "USA - Hindi",
    "GB": "UK - Hindi",
    "AE": "Middle East - Hindi",
    "QA": "Middle East - Hindi",
    "SA": "Middle East - Hindi",
    "BH": "Middle East - Hindi",
    "KW": "Middle East - Hindi",
    "OM": "Middle East - Hindi",
}

CATEGORIES = (
    "News", "Movies", "Music", "Sports", "Entertainment",
    "Lifestyle", "Infotainment", "Science", "Kids"
)

CATEGORY_MAP = {
    "news": "News",
    "movies": "Movies", "movie": "Movies",
    "music": "Music",
    "sports": "Sports",
    "entertainment": "Entertainment",
    "lifestyle": "Lifestyle",
    "infotainment": "Infotainment",
    "science": "Science",
    "kids": "Kids", "children": "Kids", "animation": "Kids",
    "documentary": "Infotainment", "education": "Infotainment",
}

# Fallback keyword mapping keeps every selected channel inside the nine JioTV-style groups.
CATEGORY_KEYWORDS = {
    "News": {"news", "breaking", "bulletin", "politics", "business news", "headlines"},
    "Movies": {"movie", "movies", "cinema", "film", "films"},
    "Music": {"music", "songs", "song", "mtv", "radio music"},
    "Sports": {"sport", "sports", "cricket", "football", "soccer", "tennis", "golf", "racing", "wrestling"},
    "Lifestyle": {"lifestyle", "food", "travel", "fashion", "home", "cooking", "cookery"},
    "Science": {"science", "technology", "tech", "space", "nature"},
    "Kids": {"kids", "children", "child", "cartoon", "animation", "junior"},
    "Infotainment": {"documentary", "education", "history", "knowledge", "discovery", "learning"},
    "Entertainment": {"entertainment", "comedy", "drama", "reality", "serial", "show"},
}


def clean(value):
    return re.sub(r"\s+", " ", str(value or "").strip())


def norm(value):
    if isinstance(value, list):
        return " ".join(norm(x) for x in value)
    if isinstance(value, dict):
        return " ".join(norm(x) for x in value.values())
    return clean(value).lower()


def fetch_json(url):
    print("Fetching:", url)
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 IPTV Playlist Generator"})
    with urlopen(request, timeout=45) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def get_languages(feed):
    return {norm(x) for x in feed.get("languages", []) if norm(x)}


def get_category(channel):
    raw_categories = channel.get("categories", [])
    for value in raw_categories:
        mapped = CATEGORY_MAP.get(norm(value))
        if mapped:
            return mapped

    text = norm([
        channel.get("name", ""), channel.get("network", ""),
        channel.get("alt_names", []), raw_categories,
    ])
    for category in CATEGORIES:
        if any(keyword in text for keyword in CATEGORY_KEYWORDS[category]):
            return category

    # No "Other" group: generic TV channels are kept under Entertainment.
    return "Entertainment"


def is_bad(channel, feed):
    text = norm([
        channel.get("id", ""), channel.get("name", ""),
        channel.get("network", ""), channel.get("alt_names", []),
        feed.get("id", ""), feed.get("name", ""), feed.get("alt_names", []),
    ])
    return any(word in text for word in BAD_WORDS)


def get_stream_feed(stream, feeds):
    stream_feed = stream.get("feed")
    if stream_feed:
        for feed in feeds:
            if str(feed.get("id", "")) == str(stream_feed):
                return feed
    for feed in feeds:
        if feed.get("is_main"):
            return feed
    return feeds[0] if feeds else {}


def get_region_group(channel, feed):
    country = clean(channel.get("country", "")).upper()
    langs = get_languages(feed)

    if country == "IN":
        if langs & REGIONAL:
            return None
        if langs & HINDI:
            return "India - Hindi"
        if langs & ENGLISH:
            return "India - English"
        if langs & BHOJPURI:
            return "India - Bhojpuri"
        return None

    if country in FOREIGN_COUNTRIES and langs & HINDI:
        return FOREIGN_COUNTRIES[country]

    return None


def build_candidates(channels, feeds, streams):
    feed_index = {}
    for feed in feeds:
        channel_id = feed.get("channel")
        if channel_id:
            feed_index.setdefault(channel_id, []).append(feed)

    stream_index = {}
    for stream in streams:
        channel_id = stream.get("channel")
        url = clean(stream.get("url", ""))
        if channel_id and url.startswith(("http://", "https://")):
            stream_index.setdefault(channel_id, []).append(stream)

    candidates = {}
    for channel in channels:
        channel_id = channel.get("id")
        if not channel_id:
            continue
        feeds_for_channel = feed_index.get(channel_id, [])
        for stream in stream_index.get(channel_id, []):
            url = clean(stream.get("url", ""))
            if not url or url in candidates:
                continue
            feed = get_stream_feed(stream, feeds_for_channel)
            if is_bad(channel, feed):
                continue
            region_group = get_region_group(channel, feed)
            if region_group is None:
                continue
            candidates[url] = {
                "channel": channel,
                "feed": feed,
                "stream": stream,
                "url": url,
                "region_group": region_group,
                "name": clean(channel.get("name", channel_id)),
                "category": get_category(channel),
            }
    return candidates


def get_headers(stream):
    headers = {
        "User-Agent": stream.get("user_agent") or
            "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 Chrome/151.0 Mobile Safari/537.36",
        "Accept": "*/*",
    }
    referrer = stream.get("referrer")
    if referrer:
        headers["Referer"] = referrer
    return headers


def check_stream(item):
    request = Request(item["url"], headers=get_headers(item["stream"]))
    try:
        with urlopen(request, timeout=TIMEOUT) as response:
            if response.status not in (200, 206):
                return False
            body = response.read(8192)
            if not body:
                return False
            text = body.decode("utf-8", errors="ignore")
            content_type = response.headers.get("Content-Type", "").lower()
            is_hls = ".m3u8" in item["url"].lower() or "#EXTM3U" in text or "mpegurl" in content_type
            return "#EXTM3U" in text if is_hls else True
    except (HTTPError, URLError, TimeoutError, ConnectionError, OSError):
        return False
    except Exception:
        return False


def sort_items(items):
    order = {name: i for i, name in enumerate(CATEGORIES)}
    return sorted(items, key=lambda x: (order[x["category"]], x["name"].lower(), x["url"]))


def write_playlist(items, path):
    items = sort_items(items)
    # Number duplicate channel URLs consistently before writing each playlist.
    totals = {}
    for item in items:
        key = (item["category"], item["name"].lower())
        totals[key] = totals.get(key, 0) + 1

    counters = {}
    with open(path, "w", encoding="utf-8") as playlist:
        playlist.write("#EXTM3U\n")
        for item in items:
            key = (item["category"], item["name"].lower())
            counters[key] = counters.get(key, 0) + 1
            n = counters[key]
            display_name = item["name"] if n == 1 else f'{item["name"]} {n}'
            channel = item["channel"]
            channel_id = clean(channel.get("id", ""))
            logo = clean(channel.get("logo", ""))
            group = item["category"]
            playlist.write(
                f'#EXTINF:-1 tvg-id="{channel_id}" tvg-name="{display_name}" '
                f'tvg-logo="{logo}" group-title="{group}",{display_name}\n'
            )
            referrer = item["stream"].get("referrer")
            user_agent = item["stream"].get("user_agent")
            if referrer:
                playlist.write(f"#EXTVLCOPT:http-referrer={referrer}\n")
            if user_agent:
                playlist.write(f"#EXTVLCOPT:http-user-agent={user_agent}\n")
            playlist.write(item["url"] + "\n")


def print_counts(title, items):
    print("\n" + title)
    print("-" * len(title))
    groups = {}
    for item in items:
        groups[item["region_group"]] = groups.get(item["region_group"], 0) + 1
    for group in ("India - Hindi", "India - English", "India - Bhojpuri", "USA - Hindi", "UK - Hindi", "Middle East - Hindi"):
        print(f"{group}: {groups.get(group, 0)}")
    print(f"TOTAL: {len(items)}")
    print("Categories:")
    cats = {}
    for item in items:
        cats[item["category"]] = cats.get(item["category"], 0) + 1
    for category in CATEGORIES:
        if cats.get(category):
            print(f"  {category}: {cats[category]}")


def main():
    print("==================================")
    print("IPTV-ORG JIOTV-STYLE PLAYLISTS")
    print("==================================")
    try:
        channels = fetch_json(CHANNELS_URL)
        feeds = fetch_json(FEEDS_URL)
        streams = fetch_json(STREAMS_URL)
    except Exception as exc:
        print("ERROR:", exc)
        sys.exit(1)

    print(f"Channels: {len(channels)}")
    print(f"Feeds: {len(feeds)}")
    print(f"Streams: {len(streams)}")

    candidates = build_candidates(channels, feeds, streams)
    items = list(candidates.values())
    print(f"Selected unique streams: {len(items)}")
    print("Checking streams...")

    working = []
    nonworking = []
    total = len(items)

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        jobs = {executor.submit(check_stream, item): item for item in items}
        for number, future in enumerate(as_completed(jobs), 1):
            item = jobs[future]
            try:
                ok = future.result()
            except Exception:
                ok = False
            (working if ok else nonworking).append(item)
            if number % 100 == 0 or number == total:
                print(f"Checked {number}/{total} | Working {len(working)} | Non-working {len(nonworking)}")

    write_playlist(working, WORKING_OUTPUT)
    write_playlist(nonworking, NONWORKING_OUTPUT)

    print("\n==================================")
    print("FINAL RESULT")
    print("==================================")
    print(f"Selected: {total}")
    print(f"Working: {len(working)} -> {WORKING_OUTPUT}")
    print(f"Non-working: {len(nonworking)} -> {NONWORKING_OUTPUT}")
    print_counts("WORKING", working)
    print_counts("NON-WORKING", nonworking)
    print("\nNo regional-language group and no Other category are generated.")


if __name__ == "__main__":
    main()
