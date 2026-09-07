#!/usr/bin/env python3

import argparse
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


CHANNELS_URL = "https://iptv-org.github.io/api/channels.json"
FEEDS_URL = "https://iptv-org.github.io/api/feeds.json"
STREAMS_URL = "https://iptv-org.github.io/api/streams.json"

DEFAULT_OUTPUT = "playlist.m3u"

# Health check is REPORT ONLY.
# It will NOT remove a channel from playlist.
HEALTH_CHECK = True
HEALTH_WORKERS = 24
HEALTH_TIMEOUT = 6


# ============================================================
# ALLOWED LANGUAGES
# ============================================================

HINDI = {"hin", "hindi"}
ENGLISH = {"eng", "english"}
BHOJPURI = {"bho", "bhojpuri"}

REGIONAL = {
    "tam", "tamil",
    "tel", "telugu",
    "ben", "bengali",
    "mar", "marathi",
    "guj", "gujarati",
    "kan", "kannada",
    "mal", "malayalam",
    "pan", "punjabi",
    "ori", "odia", "oriya",
    "asm", "assamese",
    "urd", "urdu",
    "kas", "kashmiri",
    "nep", "nepali",
    "kok", "konkani",
    "san", "sanskrit",
    "snd", "sindhi",
    "mai", "maithili",
    "doi", "dogri",
    "mni", "manipuri",
}


# ============================================================
# BAD CHANNELS
# ============================================================

BAD_WORDS = {
    "evidya",
    "pmevidya",
    "swayamprabha",
    "vandegujarat",
}


# ============================================================
# STRICT CRICKET
# ============================================================

CRICKET_NAMES = {
    "cricket gold",
    "psl tv",
    "sky sports cricket",
    "willow",
    "willow sports",
    "wplg 10.1",
}


# ============================================================
# FOREIGN HINDI NETWORKS
# ============================================================

FOREIGN_NETWORKS = {
    "colors",
    "colors cineplex",
    "colors cineplex hd",
    "colors rishtey",

    "sony sab",
    "sony sab hd",
    "sony max",
    "sony max hd",
    "sony max 2",
    "sony entertainment television",
    "sony entertainment television hd",
    "sony pal",

    "zee tv",
    "zee tv hd",
    "zee cinema",
    "zee cinema hd",
    "zee anmol",
    "zee anmol cinema",
    "zee zindagi",
    "zee classic",

    "star plus",
    "star plus hd",
    "star bharat",
    "star bharat hd",
    "star gold",
    "star gold hd",
    "star gold 2",
    "star utsav",
    "star utsav hd",
    "utsav plus",
    "utsav bharat",
}


FOREIGN_COUNTRIES = {
    "GB": "UK - Hindi",
    "US": "USA - Hindi",
    "CA": "Canada - Hindi",
    "AE": "Middle East - Hindi",
    "QA": "Middle East - Hindi",
    "SA": "Middle East - Hindi",
    "BH": "Middle East - Hindi",
    "KW": "Middle East - Hindi",
    "OM": "Middle East - Hindi",
}


# ============================================================
# CATEGORY MAP
# ============================================================

CATEGORY_MAP = {
    "news": "News",
    "music": "Music",
    "entertainment": "Entertainment",
    "lifestyle": "Lifestyle",
    "infotainment": "Infotainment",
    "science": "Science",
    "kids": "Kids",
    "children": "Kids",
    "animation": "Kids",
    "documentary": "Infotainment",
    "education": "Infotainment",
    "movies": "Entertainment",
    "movie": "Entertainment",
}


CATEGORY_PRIORITY = [
    "news",
    "music",
    "entertainment",
    "lifestyle",
    "infotainment",
    "science",
    "kids",
    "children",
    "animation",
    "documentary",
    "education",
    "movies",
    "movie",
]


# ============================================================
# HELPERS
# ============================================================

def norm(value):
    if value is None:
        return ""

    if isinstance(value, list):
        return " ".join(norm(x) for x in value)

    if isinstance(value, dict):
        return " ".join(
            norm(v) for v in value.values()
        )

    return str(value).strip().lower()


def clean_name(value):
    value = str(value or "").strip()
    value = re.sub(r"\s+", " ", value)
    return value


def get_languages(feed):
    result = set()

    for value in feed.get("languages", []):
        value = norm(value)

        if value:
            result.add(value)

    return result


def channel_text(channel, feed=None, stream=None):
    values = [
        channel.get("id", ""),
        channel.get("name", ""),
        channel.get("network", ""),
        channel.get("alt_names", []),
        channel.get("categories", []),
    ]

    if feed:
        values += [
            feed.get("id", ""),
            feed.get("name", ""),
            feed.get("alt_names", []),
            feed.get("languages", []),
        ]

    if stream:
        values += [
            stream.get("title", ""),
            stream.get("label", ""),
        ]

    return norm(values)


def is_bad(channel, feed=None):
    text = channel_text(channel, feed)

    return any(
        word in text
        for word in BAD_WORDS
    )


def has_regional(feed):
    return bool(
        get_languages(feed)
        & REGIONAL
    )


def has_hindi(feed):
    return bool(
        get_languages(feed)
        & HINDI
    )


def has_english(feed):
    return bool(
        get_languages(feed)
        & ENGLISH
    )


def has_bhojpuri(feed):
    return bool(
        get_languages(feed)
        & BHOJPURI
    )


def category(channel):
    categories = channel.get(
        "categories",
        []
    )

    for cat in categories:

        cat = norm(cat)

        if cat in CATEGORY_MAP:
            return CATEGORY_MAP[cat]

    return ""


def is_cricket(channel, feed, stream):
    name = clean_name(
        channel.get("name", "")
    ).lower()

    stream_title = clean_name(
        stream.get("title", "")
    ).lower()

    feed_name = clean_name(
        feed.get("name", "")
    ).lower()

    return (
        name in CRICKET_NAMES
        or stream_title in CRICKET_NAMES
        or feed_name in CRICKET_NAMES
    )


def get_network(channel):
    return clean_name(
        channel.get("network", "")
    ).lower()


def foreign_verified(channel):
    name = clean_name(
        channel.get("name", "")
    ).lower()

    network = get_network(channel)

    return (
        name in FOREIGN_NETWORKS
        or network in FOREIGN_NETWORKS
    )


# ============================================================
# DOWNLOAD JSON
# ============================================================

def fetch_json(url):
    print(f"Fetching: {url}")

    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 "
                "IPTV Playlist Generator"
            )
        },
    )

    with urlopen(
        request,
        timeout=45
    ) as response:

        raw = response.read()

    return json.loads(
        raw.decode(
            "utf-8",
            errors="replace"
        )
    )


# ============================================================
# INDEX FEEDS
# ============================================================

def build_feed_index(feeds):
    """
    feeds.json:
        {
            "channel": "France3.fr",
            "id": "ParisIledeFrance",
            "languages": [...]
        }

    One channel can have MANY feeds.
    """

    index = {}

    for feed in feeds:

        channel_id = feed.get(
            "channel"
        )

        if not channel_id:
            continue

        index.setdefault(
            channel_id,
            []
        ).append(feed)

    return index


# ============================================================
# STREAM INDEX
# ============================================================

def build_stream_index(streams):
    """
    streams.json:
        {
            "channel": "...",
            "feed": "...",
            "url": "..."
        }
    """

    index = {}

    for stream in streams:

        channel_id = stream.get(
            "channel"
        )

        url = stream.get(
            "url"
        )

        if not channel_id:
            continue

        if not url:
            continue

        url = str(url).strip()

        if not url.startswith(
            ("http://", "https://")
        ):
            continue

        index.setdefault(
            channel_id,
            []
        ).append(stream)

    return index


# ============================================================
# STREAM -> FEED MATCH
# ============================================================

def get_stream_feed(
    stream,
    feeds_for_channel
):
    """
    Prefer exact feed match.

    If stream.feed is empty/missing,
    still use the channel's feeds so
    language filtering does not kill the stream.
    """

    stream_feed = stream.get(
        "feed"
    )

    if stream_feed:

        for feed in feeds_for_channel:

            if str(
                feed.get("id", "")
            ) == str(stream_feed):

                return feed

    # If no exact feed is available,
    # choose main feed first.
    for feed in feeds_for_channel:

        if feed.get(
            "is_main"
        ):
            return feed

    if feeds_for_channel:
        return feeds_for_channel[0]

    return {}


# ============================================================
# GROUP DECISION
# ============================================================

def get_group(
    channel,
    feed,
    stream
):
    country = str(
        channel.get(
            "country",
            ""
        )
    ).upper()

    name = clean_name(
        channel.get(
            "name",
            ""
        )
    )

    # --------------------------------------------------------
    # CRICKET
    # --------------------------------------------------------

    if is_cricket(
        channel,
        feed,
        stream
    ):
        return "Sports - Cricket"

    # --------------------------------------------------------
    # INDIA
    # --------------------------------------------------------

    if country == "IN":

        # Explicitly reject Indian regional language.
        if has_regional(feed):
            return None

        if has_hindi(feed):
            base = "India - Hindi"

        elif has_english(feed):
            base = "India - English"

        elif has_bhojpuri(feed):
            base = "India - Bhojpuri"

        else:
            # No language = no random fallback.
            return None

        cat = category(channel)

        if cat:
            return f"{base} - {cat}"

        return base

    # --------------------------------------------------------
    # FOREIGN HINDI
    # --------------------------------------------------------

    if country in FOREIGN_COUNTRIES:

        if not has_hindi(feed):
            return None

        if not foreign_verified(channel):
            return None

        base = FOREIGN_COUNTRIES[
            country
        ]

        cat = category(channel)

        if cat:
            return f"{base} - {cat}"

        return base

    # --------------------------------------------------------
    # EVERYTHING ELSE
    # --------------------------------------------------------

    return None


# ============================================================
# HEADERS
# ============================================================

def get_headers(stream):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Linux; Android 10) "
            "AppleWebKit/537.36 "
            "Chrome/151.0 Mobile Safari/537.36"
        ),
        "Accept": "*/*",
    }

    ua = stream.get(
        "user_agent"
    )

    if ua:
        headers["User-Agent"] = ua

    referrer = stream.get(
        "referrer"
    )

    if referrer:
        headers["Referer"] = referrer

    return headers


# ============================================================
# HEALTH CHECK
# ============================================================

def health_check(item):
    url = item["url"]
    stream = item["stream"]

    request = Request(
        url,
        headers=get_headers(stream)
    )

    try:

        with urlopen(
            request,
            timeout=HEALTH_TIMEOUT
        ) as response:

            status = response.status

            body = response.read(
                8192
            )

            content_type = (
                response.headers.get(
                    "Content-Type",
                    ""
                )
                .lower()
            )

            if status not in (
                200,
                206
            ):
                return (
                    url,
                    False,
                    f"HTTP {status}"
                )

            if not body:
                return (
                    url,
                    False,
                    "EMPTY"
                )

            text = body.decode(
                "utf-8",
                errors="ignore"
            )

            is_m3u8 = (
                "#EXTM3U" in text
                or "mpegurl" in content_type
                or url.lower().endswith(
                    ".m3u8"
                )
            )

            if is_m3u8:

                if "#EXTM3U" not in text:
                    return (
                        url,
                        False,
                        "BAD M3U8"
                    )

                return (
                    url,
                    True,
                    "M3U8 OK"
                )

            return (
                url,
                True,
                f"HTTP {status}"
            )

    except HTTPError as e:

        return (
            url,
            False,
            f"HTTP {e.code}"
        )

    except (
        URLError,
        TimeoutError,
        ConnectionError
    ):

        return (
            url,
            False,
            "TIMEOUT/CONNECTION"
        )

    except Exception as e:

        return (
            url,
            False,
            type(e).__name__
        )


# ============================================================
# NAME NUMBERING
# ============================================================

def numbered_name(
    group,
    name,
    counters
):
    key = (
        group,
        name.lower()
    )

    counters[key] = (
        counters.get(key, 0) + 1
    )

    number = counters[key]

    if number == 1:
        return name

    return f"{name} {number}"


# ============================================================
# M3U
# ============================================================

def m3u_entry(item, display_name):
    channel = item["channel"]

    channel_id = channel.get(
        "id",
        ""
    )

    logo = channel.get(
        "logo",
        ""
    )

    group = item["group"]
    url = item["url"]

    return (
        f'#EXTINF:-1 '
        f'tvg-id="{channel_id}" '
        f'tvg-name="{display_name}" '
        f'tvg-logo="{logo}" '
        f'group-title="{group}",'
        f'{display_name}\n'
        f'{url}\n'
    )


# ============================================================
# BUILD
# ============================================================

def build(
    channels,
    feeds,
    streams
):
    feed_index = build_feed_index(
        feeds
    )

    stream_index = build_stream_index(
        streams
    )

    stats = {
        "channels": len(channels),
        "feeds": len(feeds),
        "streams": len(streams),
        "eligible": 0,
        "duplicate_urls": 0,
        "regional": 0,
        "not_allowed": 0,
        "no_stream": 0,
        "working": 0,
        "failed": 0,
    }

    # URL is the global identity.
    candidates = {}

    # --------------------------------------------------------
    # WALK CHANNELS
    # --------------------------------------------------------

    for channel in channels:

        channel_id = channel.get(
            "id"
        )

        if not channel_id:
            continue

        channel_name = clean_name(
            channel.get(
                "name",
                channel_id
            )
        )

        feeds_for_channel = feed_index.get(
            channel_id,
            []
        )

        streams_for_channel = stream_index.get(
            channel_id,
            []
        )

        if not streams_for_channel:
            stats["no_stream"] += 1
            continue

        # ----------------------------------------------------
        # Every stream is considered separately.
        # This is important:
        #
        # Same channel + different URL = KEEP BOTH.
        # Same URL globally = KEEP ONE.
        # ----------------------------------------------------

        for stream in streams_for_channel:

            url = str(
                stream.get(
                    "url",
                    ""
                )
            ).strip()

            if not url:
                continue

            feed = get_stream_feed(
                stream,
                feeds_for_channel
            )

            # Bad educational/public channels
            if is_bad(
                channel,
                feed
            ):
                stats["not_allowed"] += 1
                continue

            group = get_group(
                channel,
                feed,
                stream
            )

            if group is None:

                # Count regional separately
                country = str(
                    channel.get(
                        "country",
                        ""
                    )
                ).upper()

                if (
                    country == "IN"
                    and has_regional(feed)
                ):
                    stats["regional"] += 1
                else:
                    stats["not_allowed"] += 1

                continue

            # ------------------------------------------------
            # GLOBAL EXACT URL DEDUP
            # ------------------------------------------------

            if url in candidates:

                stats["duplicate_urls"] += 1
                continue

            candidates[url] = {
                "url": url,
                "channel": channel,
                "feed": feed,
                "stream": stream,
                "group": group,
                "name": channel_name,
            }

    stats["eligible"] = len(
        candidates
    )

    return candidates, stats


# ============================================================
# WRITE
# ============================================================

def write_playlist(
    candidates,
    output
):
    counters = {}

    items = list(
        candidates.values()
    )

    items.sort(
        key=lambda x: (
            x["group"].lower(),
            x["name"].lower(),
            x["url"]
        )
    )

    with open(
        output,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "#EXTM3U\n"
        )

        for item in items:

            name = numbered_name(
                item["group"],
                item["name"],
                counters
            )

            f.write(
                m3u_entry(
                    item,
                    name
                )
            )

    return items


# ============================================================
# HEALTH REPORT
# ============================================================

def run_health_check(
    candidates
):
    if not candidates:
        return

    print()
    print(
        "----------------------------------"
    )
    print(
        f"HEALTH CHECK: "
        f"{len(candidates)} unique streams"
    )
    print(
        "REPORT ONLY - "
        "FAILED STREAMS WILL NOT BE REMOVED"
    )
    print(
        "----------------------------------"
    )

    working = 0
    failed = 0

    started = time.time()

    with ThreadPoolExecutor(
        max_workers=HEALTH_WORKERS
    ) as executor:

        jobs = [
            executor.submit(
                health_check,
                item
            )
            for item in candidates.values()
        ]

        total = len(jobs)

        for number, future in enumerate(
            as_completed(jobs),
            1
        ):

            try:
                url, ok, reason = (
                    future.result()
                )
            except Exception:
                ok = False
                reason = "ERROR"

            if ok:
                working += 1
            else:
                failed += 1

            if (
                number % 100 == 0
                or number == total
            ):
                print(
                    f"Checked {number}/{total} | "
                    f"Working {working} | "
                    f"Failed {failed}"
                )

    elapsed = time.time() - started

    print(
        f"Health check finished in "
        f"{elapsed:.1f}s"
    )

    print(
        f"Working: {working}"
    )

    print(
        f"Failed: {failed}"
    )


# ============================================================
# GROUP STATS
# ============================================================

def print_groups(items):
    groups = {}

    for item in items:

        group = item["group"]

        groups[group] = (
            groups.get(group, 0) + 1
        )

    print()
    print(
        "=================================="
    )
    print(
        "GROUPS"
    )
    print(
        "=================================="
    )

    for group in sorted(
        groups
    ):

        print(
            f"{group}: {groups[group]}"
        )

    print(
        "----------------------------------"
    )

    print(
        f"TOTAL: {len(items)}"
    )

    print(
        "=================================="
    )


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "source",
        nargs="?",
        default="sources"
    )

    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_OUTPUT
    )

    parser.add_argument(
        "--no-health-check",
        action="store_true"
    )

    args = parser.parse_args()

    print(
        "IPTV Playlist Generator"
    )

    print(
        "Source: IPTV-org API"
    )

    print()

    try:

        channels = fetch_json(
            CHANNELS_URL
        )

        feeds = fetch_json(
            FEEDS_URL
        )

        streams = fetch_json(
            STREAMS_URL
        )

    except Exception as e:

        print(
            f"\nERROR: {e}"
        )

        sys.exit(1)

    print()
    print(
        f"Channels API: {len(channels)}"
    )

    print(
        f"Feeds API: {len(feeds)}"
    )

    print(
        f"Streams API: {len(streams)}"
    )

    print()

    candidates, stats = build(
        channels,
        feeds,
        streams
    )

    print(
        "----------------------------------"
    )

    print(
        f"Channels scanned: "
        f"{stats['channels']}"
    )

    print(
        f"Streams mapped: "
        f"{stats['streams']}"
    )

    print(
        f"Eligible unique URLs: "
        f"{stats['eligible']}"
    )

    print(
        f"Duplicate URLs removed: "
        f"{stats['duplicate_urls']}"
    )

    print(
        f"Regional removed: "
        f"{stats['regional']}"
    )

    print(
        f"Not allowed: "
        f"{stats['not_allowed']}"
    )

    print(
        f"Channels without streams: "
        f"{stats['no_stream']}"
    )

    print(
        "----------------------------------"
    )

    # IMPORTANT:
    # Health check NEVER filters playlist.
    if (
        HEALTH_CHECK
        and not args.no_health_check
    ):
        run_health_check(
            candidates
        )

    items = write_playlist(
        candidates,
        args.output
    )

    print_groups(
        items
    )

    print(
        f"PLAYLIST: {args.output}"
    )


if __name__ == "__main__":
    main()
