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

OUTPUT = "playlist.m3u"

WORKERS = 24
TIMEOUT = 8


# ============================================================
# LANGUAGES
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
# FOREIGN HINDI
# ============================================================

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


# ============================================================
# JIOTV STYLE CATEGORY
# ============================================================

CATEGORY_MAP = {
    "news": "News",

    "movies": "Movies",
    "movie": "Movies",

    "music": "Music",

    "sports": "Sports",

    "entertainment": "Entertainment",

    "lifestyle": "Lifestyle",

    "infotainment": "Infotainment",

    "science": "Science",

    "kids": "Kids",
    "children": "Kids",
    "animation": "Kids",

    "documentary": "Infotainment",
    "education": "Infotainment",
}


CATEGORY_ORDER = [
    "News",
    "Movies",
    "Music",
    "Sports",
    "Entertainment",
    "Lifestyle",
    "Infotainment",
    "Science",
    "Kids",
    "Other",
]


# ============================================================
# HELPERS
# ============================================================

def clean(value):
    return re.sub(
        r"\s+",
        " ",
        str(value or "").strip()
    )


def norm(value):

    if isinstance(value, list):
        return " ".join(
            norm(x) for x in value
        )

    if isinstance(value, dict):
        return " ".join(
            norm(x)
            for x in value.values()
        )

    return clean(value).lower()


def fetch_json(url):

    print("Fetching:", url)

    request = Request(
        url,
        headers={
            "User-Agent":
                "Mozilla/5.0 IPTV Playlist Generator"
        }
    )

    with urlopen(
        request,
        timeout=45
    ) as response:

        data = response.read()

    return json.loads(
        data.decode(
            "utf-8",
            errors="replace"
        )
    )


# ============================================================
# FEED LANGUAGE
# ============================================================

def get_languages(feed):

    result = set()

    for value in feed.get(
        "languages",
        []
    ):

        value = norm(value)

        if value:
            result.add(value)

    return result


# ============================================================
# CATEGORY
# ============================================================

def get_category(channel):

    for value in channel.get(
        "categories",
        []
    ):

        value = norm(value)

        if value in CATEGORY_MAP:
            return CATEGORY_MAP[value]

    return "Other"


# ============================================================
# BAD CHANNEL CHECK
# ============================================================

def is_bad(channel, feed):

    text = norm([
        channel.get("id", ""),
        channel.get("name", ""),
        channel.get("network", ""),
        channel.get("alt_names", []),

        feed.get("id", ""),
        feed.get("name", ""),
        feed.get("alt_names", []),
    ])

    return any(
        word in text
        for word in BAD_WORDS
    )


# ============================================================
# STREAM -> FEED
# ============================================================

def get_stream_feed(
    stream,
    feeds
):

    stream_feed = stream.get(
        "feed"
    )

    if stream_feed:

        for feed in feeds:

            if str(
                feed.get("id", "")
            ) == str(stream_feed):

                return feed

    # Prefer main feed
    for feed in feeds:

        if feed.get("is_main"):
            return feed

    if feeds:
        return feeds[0]

    return {}


# ============================================================
# LANGUAGE SELECTION
# ============================================================

def get_region_group(
    channel,
    feed
):

    country = clean(
        channel.get(
            "country",
            ""
        )
    ).upper()

    langs = get_languages(feed)

    # --------------------------------------------------------
    # INDIA
    # --------------------------------------------------------

    if country == "IN":

        # Reject Indian regional languages
        if langs & REGIONAL:
            return None

        if langs & HINDI:
            return "India - Hindi"

        if langs & ENGLISH:
            return "India - English"

        if langs & BHOJPURI:
            return "India - Bhojpuri"

        return None

    # --------------------------------------------------------
    # FOREIGN HINDI
    # --------------------------------------------------------

    if country in FOREIGN_COUNTRIES:

        if langs & HINDI:
            return FOREIGN_COUNTRIES[
                country
            ]

        return None

    return None


# ============================================================
# BUILD CANDIDATES
# ============================================================

def build_candidates(
    channels,
    feeds,
    streams
):

    feed_index = {}

    for feed in feeds:

        channel_id = feed.get(
            "channel"
        )

        if channel_id:

            feed_index.setdefault(
                channel_id,
                []
            ).append(feed)

    stream_index = {}

    for stream in streams:

        channel_id = stream.get(
            "channel"
        )

        url = clean(
            stream.get(
                "url",
                ""
            )
        )

        if (
            channel_id
            and url.startswith(
                (
                    "http://",
                    "https://"
                )
            )
        ):

            stream_index.setdefault(
                channel_id,
                []
            ).append(stream)

    candidates = {}

    for channel in channels:

        channel_id = channel.get(
            "id"
        )

        if not channel_id:
            continue

        feeds_for_channel = (
            feed_index.get(
                channel_id,
                []
            )
        )

        streams_for_channel = (
            stream_index.get(
                channel_id,
                []
            )
        )

        for stream in streams_for_channel:

            url = clean(
                stream.get(
                    "url",
                    ""
                )
            )

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
                continue

            region_group = get_region_group(
                channel,
                feed
            )

            if region_group is None:
                continue

            # Same URL globally = one entry
            if url in candidates:
                continue

            candidates[url] = {
                "channel": channel,
                "feed": feed,
                "stream": stream,
                "url": url,
                "region_group": region_group,
                "name": clean(
                    channel.get(
                        "name",
                        channel_id
                    )
                ),
                "category": get_category(
                    channel
                ),
            }

    return candidates


# ============================================================
# STREAM HEADERS
# ============================================================

def get_headers(stream):

    headers = {
        "User-Agent":
            stream.get(
                "user_agent"
            )
            or
            "Mozilla/5.0 "
            "(Linux; Android 10) "
            "AppleWebKit/537.36 "
            "Chrome/151.0 Mobile Safari/537.36",

        "Accept": "*/*",
    }

    referrer = stream.get(
        "referrer"
    )

    if referrer:
        headers["Referer"] = referrer

    return headers


# ============================================================
# WORKING CHECK
# ============================================================

def check_stream(item):

    url = item["url"]

    stream = item["stream"]

    request = Request(
        url,
        headers=get_headers(stream)
    )

    try:

        with urlopen(
            request,
            timeout=TIMEOUT
        ) as response:

            status = response.status

            if status not in (
                200,
                206
            ):
                return False

            body = response.read(
                8192
            )

            if not body:
                return False

            text = body.decode(
                "utf-8",
                errors="ignore"
            )

            content_type = (
                response.headers.get(
                    "Content-Type",
                    ""
                )
                .lower()
            )

            # HLS
            if (
                ".m3u8"
                in url.lower()
                or
                "#EXTM3U"
                in text
                or
                "mpegurl"
                in content_type
            ):

                return (
                    "#EXTM3U"
                    in text
                )

            # Other stream response
            return True

    except (
        HTTPError,
        URLError,
        TimeoutError,
        ConnectionError
    ):

        return False

    except Exception:

        return False


# ============================================================
# WRITE PLAYLIST
# ============================================================

def write_playlist(
    working
):

    order = {
        name: number
        for number, name
        in enumerate(
            CATEGORY_ORDER
        )
    }

    working.sort(
        key=lambda x: (
            order.get(
                x["category"],
                99
            ),
            x["name"].lower(),
            x["url"]
        )
    )

    counters = {}

    with open(
        OUTPUT,
        "w",
        encoding="utf-8"
    ) as playlist:

        playlist.write(
            "#EXTM3U\n"
        )

        for item in working:

            key = (
                item["category"],
                item["name"].lower()
            )

            counters[key] = (
                counters.get(
                    key,
                    0
                ) + 1
            )

            number = counters[key]

            if number == 1:
                display_name = item["name"]
            else:
                display_name = (
                    f'{item["name"]} '
                    f'{number}'
                )

            channel = item[
                "channel"
            ]

            channel_id = clean(
                channel.get(
                    "id",
                    ""
                )
            )

            logo = clean(
                channel.get(
                    "logo",
                    ""
                )
            )

            group = item[
                "category"
            ]

            playlist.write(
                f'#EXTINF:-1 '
                f'tvg-id="{channel_id}" '
                f'tvg-name="{display_name}" '
                f'tvg-logo="{logo}" '
                f'group-title="{group}",'
                f'{display_name}\n'
            )

            playlist.write(
                item["url"]
                + "\n"
            )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print(
        "=================================="
    )
    print(
        "IPTV-ORG WORKING CHANNEL PLAYLIST"
    )
    print(
        "=================================="
    )

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

        print()
        print(
            "ERROR:",
            e
        )

        sys.exit(1)

    print()
    print(
        "Channels:",
        len(channels)
    )

    print(
        "Feeds:",
        len(feeds)
    )

    print(
        "Streams:",
        len(streams)
    )

    candidates = build_candidates(
        channels,
        feeds,
        streams
    )

    print()
    print(
        "Selected streams:",
        len(candidates)
    )

    print()
    print(
        "Checking streams..."
    )

    working = []

    failed = 0

    total = len(candidates)

    with ThreadPoolExecutor(
        max_workers=WORKERS
    ) as executor:

        jobs = {
            executor.submit(
                check_stream,
                item
            ): item

            for item
            in candidates.values()
        }

        for number, future in enumerate(
            as_completed(jobs),
            1
        ):

            item = jobs[
                future
            ]

            try:

                ok = future.result()

            except Exception:

                ok = False

            if ok:

                working.append(
                    item
                )

            else:

                failed += 1

            if (
                number % 100 == 0
                or
                number == total
            ):

                print(
                    f"Checked "
                    f"{number}/{total} | "
                    f"Working "
                    f"{len(working)} | "
                    f"Failed "
                    f"{failed}"
                )

    write_playlist(
        working
    )

    print()
    print(
        "=================================="
    )
    print(
        "FINAL RESULT"
    )
    print(
        "=================================="
    )

    print(
        "Selected:",
        total
    )

    print(
        "Working:",
        len(working)
    )

    print(
        "Non-working:",
        failed
    )

    print(
        "Playlist:",
        OUTPUT
    )

    print(
        "----------------------------------"
    )

    category_count = {}

    for item in working:

        category = item[
            "category"
        ]

        category_count[
            category
        ] = (
            category_count.get(
                category,
                0
            ) + 1
        )

    for category in CATEGORY_ORDER:

        if category_count.get(
            category,
            0
        ):

            print(
                f"{category}: "
                f"{category_count[category]}"
            )

    print(
        "=================================="
    )


if __name__ == "__main__":
    main()
