#!/usr/bin/env python3

import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# ============================================================
# CONFIG
# ============================================================

CHANNELS_URL = "https://iptv-org.github.io/api/channels.json"
FEEDS_URL    = "https://iptv-org.github.io/api/feeds.json"
STREAMS_URL  = "https://iptv-org.github.io/api/streams.json"

OUTPUT_FILE = "playlist.m3u"

HEALTH_CHECK = True
MAX_WORKERS = 20
TIMEOUT = 8

# ============================================================
# GROUP ORDER
# ============================================================

GROUP_ORDER = [
    "India - Hindi",
    "India - Hindi - News",
    "India - Hindi - Music",
    "India - Hindi - Entertainment",
    "India - Hindi - Lifestyle",
    "India - Hindi - Infotainment",
    "India - Hindi - Science",
    "India - Hindi - Kids",

    "India - English",
    "India - English - News",
    "India - English - Music",
    "India - English - Entertainment",
    "India - English - Lifestyle",
    "India - English - Infotainment",
    "India - English - Science",
    "India - English - Kids",

    "India - Bhojpuri",
    "India - Bhojpuri - News",
    "India - Bhojpuri - Music",
    "India - Bhojpuri - Entertainment",

    "UK - Hindi",
    "UK - Hindi - News",
    "UK - Hindi - Music",
    "UK - Hindi - Entertainment",

    "USA - Hindi",
    "USA - Hindi - News",
    "USA - Hindi - Music",
    "USA - Hindi - Entertainment",

    "Canada - Hindi",
    "Canada - Hindi - News",
    "Canada - Hindi - Music",
    "Canada - Hindi - Entertainment",

    "Middle East - Hindi",
    "Middle East - Hindi - News",
    "Middle East - Hindi - Music",
    "Middle East - Hindi - Entertainment",

    "Sports - Cricket",
    "Radio - Hindi",
]

# ============================================================
# LANGUAGE
# ============================================================

HINDI = {
    "hindi",
    "hin",
}

ENGLISH = {
    "english",
    "eng",
}

BHOJPURI = {
    "bhojpuri",
    "bho",
}

# ============================================================
# INDIAN REGIONAL LANGUAGES
# ============================================================

REGIONAL = {
    "tamil", "tam",
    "telugu", "tel",
    "bengali", "ben",
    "marathi", "mar",
    "gujarati", "guj",
    "kannada", "kan",
    "malayalam", "mal",
    "punjabi", "pan",
    "odia", "oriya", "ori",
    "assamese", "asm",
    "urdu", "urd",
    "kashmiri", "kas",
    "nepali", "nep",
    "konkani", "kok",
    "sanskrit", "san",
    "sindhi", "snd",
    "maithili", "mai",
    "dogri", "doi",
    "manipuri", "mni",
}

# ============================================================
# BAD CHANNEL NAMES
# ============================================================

BAD_WORDS = (
    "evidya",
    "pmevidya",
    "swayamprabha",
    "vandegujarat",
)

# ============================================================
# STRICT CRICKET CHANNELS
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
# FOREIGN COUNTRIES
# ============================================================

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
# FOREIGN VERIFIED NETWORKS
# ============================================================

FOREIGN_NETWORKS = {
    # COLORS
    "colors",
    "colors cineplex",
    "colors cineplex hd",
    "colors rishtey",

    # SONY
    "sony sab",
    "sony sab hd",
    "sony max",
    "sony max hd",
    "sony max 2",
    "sony entertainment television",
    "sony entertainment television hd",
    "sony pal",

    # ZEE
    "zee tv",
    "zee tv hd",
    "zee cinema",
    "zee cinema hd",
    "zee anmol",
    "zee anmol cinema",
    "zee zindagi",
    "zee classic",

    # STAR
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

# ============================================================
# JIOTV STYLE CATEGORIES
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

    # Common IPTV-org category names
    "movies": "Entertainment",
    "movie": "Entertainment",
    "documentary": "Infotainment",
    "education": "Infotainment",
    "animation": "Kids",
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
    "movies",
    "movie",
    "documentary",
    "education",
    "animation",
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
            f"{norm(k)} {norm(v)}"
            for k, v in value.items()
        )

    return str(value).strip().lower()


def clean_name(value):
    if not value:
        return "Unknown"

    value = str(value).strip()
    value = re.sub(r"\s+", " ", value)

    return value


def get_name(obj):
    for key in ("name", "title", "channelName", "channel_name"):
        value = obj.get(key)

        if value:
            return clean_name(value)

    return "Unknown"


def get_id(obj):
    for key in ("id", "channel", "channelId", "channel_id"):
        value = obj.get(key)

        if value is not None:
            return str(value)

    return ""


def get_languages(obj):
    values = []

    for key in (
        "languages",
        "language",
        "lang",
    ):
        value = obj.get(key)

        if isinstance(value, list):
            values.extend(value)

        elif value:
            values.append(value)

    return {
        norm(x)
        for x in values
        if norm(x)
    }


def get_country(obj):
    for key in (
        "country",
        "countryCode",
        "country_code",
    ):
        value = obj.get(key)

        if isinstance(value, list):
            for item in value:
                item = str(item).upper().strip()

                if item:
                    return item

        elif value:
            return str(value).upper().strip()

    return ""


def get_categories(obj):
    values = []

    for key in (
        "categories",
        "category",
        "genres",
        "genre",
    ):
        value = obj.get(key)

        if isinstance(value, list):
            values.extend(value)

        elif value:
            values.append(value)

    result = []

    for value in values:
        value = norm(value)

        if value:
            result.append(value)

    return result


def get_network(obj):
    for key in (
        "network",
        "networkName",
        "network_name",
    ):
        value = obj.get(key)

        if value:
            return clean_name(value)

    return ""


def get_stream_url(obj):
    for key in (
        "url",
        "stream",
        "stream_url",
        "streamUrl",
        "play_url",
        "playUrl",
    ):
        value = obj.get(key)

        if isinstance(value, str):
            value = value.strip()

            if value.startswith(("http://", "https://")):
                return value

    return ""


def combined_text(channel, feed=None, stream=None):
    parts = [
        get_name(channel),
        get_network(channel),
        norm(channel.get("languages")),
        norm(channel.get("categories")),
    ]

    if feed:
        parts.extend([
            get_name(feed),
            get_network(feed),
            norm(feed),
        ])

    if stream:
        parts.extend([
            norm(stream),
        ])

    return " ".join(parts).lower()


def is_bad(channel, feed=None):
    text = combined_text(channel, feed)

    return any(
        word in text
        for word in BAD_WORDS
    )


def has_regional_language(channel, feed=None):
    languages = set(
        get_languages(channel)
    )

    if feed:
        languages.update(
            get_languages(feed)
        )

    return bool(
        languages.intersection(REGIONAL)
    )


def has_hindi(channel, feed=None):
    languages = set(
        get_languages(channel)
    )

    if feed:
        languages.update(
            get_languages(feed)
        )

    if languages.intersection(HINDI):
        return True

    text = combined_text(channel, feed)

    return bool(
        re.search(
            r"\bhindi\b|\bhindustani\b",
            text,
            re.I
        )
    )


def has_english(channel, feed=None):
    languages = set(
        get_languages(channel)
    )

    if feed:
        languages.update(
            get_languages(feed)
        )

    return bool(
        languages.intersection(ENGLISH)
    )


def has_bhojpuri(channel, feed=None):
    languages = set(
        get_languages(channel)
    )

    if feed:
        languages.update(
            get_languages(feed)
        )

    return bool(
        languages.intersection(BHOJPURI)
    )


def cricket_channel(channel, feed=None):
    name = get_name(channel).lower().strip()

    if name in CRICKET_NAMES:
        return True

    if feed:
        feed_name = get_name(feed).lower().strip()

        if feed_name in CRICKET_NAMES:
            return True

    return False


def get_category(channel, feed=None):
    categories = get_categories(channel)

    if feed:
        categories.extend(
            get_categories(feed)
        )

    # Also inspect raw text for category names.
    raw = combined_text(
        channel,
        feed
    )

    for category in CATEGORY_PRIORITY:
        if category in categories:
            return CATEGORY_MAP[category]

    for category in CATEGORY_PRIORITY:
        if re.search(
            rf"\b{re.escape(category)}\b",
            raw,
            re.I
        ):
            return CATEGORY_MAP[category]

    return ""


# ============================================================
# FETCH JSON
# ============================================================

def fetch_json(url):
    print(f"Fetching: {url}")

    req = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 "
                "Android IPTV Playlist Generator"
            )
        },
    )

    with urlopen(
        req,
        timeout=30
    ) as response:

        data = response.read()

    return json.loads(
        data.decode(
            "utf-8",
            errors="replace"
        )
    )


# ============================================================
# INDEXES
# ============================================================

def build_feed_index(feeds):
    index = {}

    for feed in feeds:

        cid = get_id(feed)

        if not cid:
            cid = str(
                feed.get("channel", "")
            )

        if not cid:
            continue

        index.setdefault(
            cid,
            []
        ).append(feed)

    return index


def build_stream_index(streams):
    index = {}

    for stream in streams:

        cid = get_id(stream)

        if not cid:
            continue

        url = get_stream_url(stream)

        if not url:
            continue

        index.setdefault(
            cid,
            []
        ).append(stream)

    return index


# ============================================================
# M3U ENTRY
# ============================================================

def make_entry(
    group,
    name,
    channel_id,
    logo,
    url
):
    logo = logo or ""

    return (
        f'#EXTINF:-1 tvg-id="{channel_id}" '
        f'tvg-name="{name}" '
        f'tvg-logo="{logo}" '
        f'group-title="{group}",{name}\n'
        f'{url}\n'
    )


# ============================================================
# STREAM HEADERS
# ============================================================

def stream_headers(stream=None):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Linux; Android 10) "
            "AppleWebKit/537.36 "
            "Chrome/151.0 Mobile Safari/537.36"
        ),
        "Accept": (
            "application/vnd.apple.mpegurl,"
            "application/x-mpegURL,"
            "video/*,"
            "*/*"
        ),
    }

    if not stream:
        return headers

    for key in (
        "user_agent",
        "user-agent",
        "userAgent",
    ):
        value = stream.get(key)

        if value:
            headers["User-Agent"] = str(value)
            break

    for key in (
        "referrer",
        "referer",
        "http_referrer",
        "http-referrer",
    ):
        value = stream.get(key)

        if value:
            headers["Referer"] = str(value)
            break

    origin = stream.get("origin")

    if origin:
        headers["Origin"] = str(origin)

    return headers


# ============================================================
# HTTP READ
# ============================================================

def http_read(url, stream=None, limit=65536):
    headers = stream_headers(stream)

    req = Request(
        url,
        headers=headers
    )

    try:
        with urlopen(
            req,
            timeout=TIMEOUT
        ) as response:

            status = response.status
            content_type = (
                response.headers.get(
                    "Content-Type",
                    ""
                )
                .lower()
            )

            body = response.read(
                limit
            )

            final_url = response.geturl()

            return (
                True,
                status,
                content_type,
                body,
                final_url,
            )

    except HTTPError as e:
        return (
            False,
            e.code,
            "",
            b"",
            url,
        )

    except (
        URLError,
        TimeoutError,
        ConnectionError,
    ):
        return (
            False,
            0,
            "",
            b"",
            url,
        )

    except Exception:
        return (
            False,
            0,
            "",
            b"",
            url,
        )


# ============================================================
# HLS CHECK
# ============================================================

def check_hls(
    url,
    stream=None,
    body=None,
    content_type=""
):
    if body is None:
        ok, status, content_type, body, final_url = (
            http_read(
                url,
                stream
            )
        )

        if not ok:
            return False, f"HTTP {status}"

        url = final_url

    text = body.decode(
        "utf-8",
        errors="ignore"
    )

    if "#EXTM3U" not in text:
        return False, "Not M3U8"

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # Master playlist
    if "#EXT-X-STREAM-INF" in text:

        variant = ""

        for i, line in enumerate(lines):

            if line.startswith(
                "#EXT-X-STREAM-INF"
            ):
                for next_line in lines[i + 1:]:

                    if (
                        not next_line.startswith(
                            "#"
                        )
                    ):
                        variant = next_line
                        break

                if variant:
                    break

        if variant:

            variant_url = urljoin(
                url,
                variant
            )

            ok, status, ctype, variant_body, final_url = (
                http_read(
                    variant_url,
                    stream
                )
            )

            if not ok:
                return (
                    False,
                    f"Variant HTTP {status}"
                )

            variant_text = variant_body.decode(
                "utf-8",
                errors="ignore"
            )

            if "#EXTM3U" not in variant_text:
                return (
                    False,
                    "Invalid variant"
                )

            text = variant_text
            url = final_url
            lines = [
                line.strip()
                for line in text.splitlines()
                if line.strip()
            ]

    # Media playlist
    segment = ""

    for line in lines:

        if line.startswith("#"):
            continue

        if (
            line.startswith(
                "http://"
            )
            or line.startswith(
                "https://"
            )
            or line.startswith("/")
            or "." in line
        ):
            segment = line
            break

    if not segment:
        # A valid live playlist may temporarily
        # contain no segment yet.
        if (
            "#EXT-X-TARGETDURATION" in text
            or "#EXT-X-MEDIA-SEQUENCE" in text
        ):
            return True, "Valid HLS"

        return False, "No HLS media"

    segment_url = urljoin(
        url,
        segment
    )

    ok, status, ctype, segment_body, final_url = (
        http_read(
            segment_url,
            stream,
            limit=4096
        )
    )

    if not ok:
        return (
            False,
            f"Segment HTTP {status}"
        )

    if not segment_body:
        return False, "Empty segment"

    return True, "HLS OK"


# ============================================================
# COMPLETE STREAM HEALTH CHECK
# ============================================================

def check_stream(item):
    url = item["url"]
    stream = item.get("stream")

    ok, status, content_type, body, final_url = (
        http_read(
            url,
            stream
        )
    )

    if not ok:
        return (
            url,
            False,
            f"HTTP {status}"
        )

    if status not in (
        200,
        206,
    ):
        return (
            url,
            False,
            f"HTTP {status}"
        )

    text_head = body[:4096].decode(
        "utf-8",
        errors="ignore"
    )

    is_hls = (
        "#EXTM3U" in text_head
        or "mpegurl" in content_type
        or "vnd.apple.mpegurl" in content_type
        or url.lower().split("?")[0].endswith(
            ".m3u8"
        )
    )

    if is_hls:

        ok, reason = check_hls(
            final_url,
            stream,
            body,
            content_type
        )

        return (
            url,
            ok,
            reason
        )

    if not body:
        return (
            url,
            False,
            "Empty response"
        )

    # Reject obvious HTML error pages.
    lower = text_head.lower()

    if (
        "<html" in lower
        or "<!doctype html" in lower
    ):
        return (
            url,
            False,
            "HTML response"
        )

    return (
        url,
        True,
        f"HTTP {status}"
    )


# ============================================================
# UNIQUE NAME
# ============================================================

def unique_name(
    group,
    base_name,
    counters
):
    key = (
        group,
        base_name.lower().strip()
    )

    counters[key] = (
        counters.get(key, 0) + 1
    )

    number = counters[key]

    if number == 1:
        return base_name

    return f"{base_name} {number}"


# ============================================================
# BUILD PLAYLIST
# ============================================================

def build_playlist(
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
        "regional_removed": 0,
        "bad_removed": 0,
        "not_allowed": 0,
        "no_url": 0,
        "duplicate_urls": 0,
        "health_failed": 0,
        "health_working": 0,
    }

    # --------------------------------------------------------
    # Candidate collection
    # --------------------------------------------------------

    candidates = {}
    # URL -> item
    #
    # This globally removes exact duplicate URLs BEFORE
    # health checking.
    #
    # If the same channel has another URL, that URL survives.

    for channel in channels:

        cid = get_id(channel)

        if not cid:
            continue

        name = get_name(channel)

        if name == "Unknown":
            continue

        channel_feeds = feed_index.get(
            cid,
            []
        )

        channel_streams = stream_index.get(
            cid,
            []
        )

        # ----------------------------------------------------
        # Build stream list.
        # Feed URL first, then streams.json.
        # ----------------------------------------------------

        source_items = []

        for feed in channel_feeds:

            url = get_stream_url(feed)

            if url:
                source_items.append(
                    (
                        url,
                        feed
                    )
                )

        for stream in channel_streams:

            url = get_stream_url(stream)

            if url:
                source_items.append(
                    (
                        url,
                        stream
                    )
                )

        if not source_items:
            stats["no_url"] += 1
            continue

        # ----------------------------------------------------
        # Bad channels
        # ----------------------------------------------------

        if is_bad(
            channel,
            channel_feeds[0]
            if channel_feeds
            else None
        ):
            stats["bad_removed"] += 1
            continue

        country = get_country(
            channel
        )

        # ====================================================
        # CRICKET
        # ====================================================

        if cricket_channel(
            channel,
            channel_feeds[0]
            if channel_feeds
            else None
        ):

            group = "Sports - Cricket"

        # ====================================================
        # INDIA
        # ====================================================

        elif country == "IN":

            # NEVER add Indian regional channels.
            if has_regional_language(
                channel,
                channel_feeds[0]
                if channel_feeds
                else None
            ):
                stats["regional_removed"] += 1
                continue

            if has_hindi(
                channel,
                channel_feeds[0]
                if channel_feeds
                else None
            ):
                base_group = "India - Hindi"

            elif has_english(
                channel,
                channel_feeds[0]
                if channel_feeds
                else None
            ):
                base_group = "India - English"

            elif has_bhojpuri(
                channel,
                channel_feeds[0]
                if channel_feeds
                else None
            ):
                base_group = "India - Bhojpuri"

            else:
                # NO RANDOM FALLBACK.
                stats["not_allowed"] += 1
                continue

            category = get_category(
                channel,
                channel_feeds[0]
                if channel_feeds
                else None
            )

            if category:
                group = (
                    f"{base_group} - {category}"
                )
            else:
                group = base_group

        # ====================================================
        # FOREIGN HINDI
        # ====================================================

        elif country in FOREIGN_COUNTRIES:

            if not has_hindi(
                channel,
                channel_feeds[0]
                if channel_feeds
                else None
            ):
                stats["not_allowed"] += 1
                continue

            network = get_network(
                channel
            ).lower().strip()

            channel_name = name.lower().strip()

            verified = (
                network in FOREIGN_NETWORKS
                or channel_name in FOREIGN_NETWORKS
            )

            if not verified:
                stats["not_allowed"] += 1
                continue

            base_group = FOREIGN_COUNTRIES[
                country
            ]

            category = get_category(
                channel,
                channel_feeds[0]
                if channel_feeds
                else None
            )

            if category:
                group = (
                    f"{base_group} - {category}"
                )
            else:
                group = base_group

        else:
            # No random country channels.
            stats["not_allowed"] += 1
            continue

        # ----------------------------------------------------
        # Candidate per URL
        # ----------------------------------------------------

        logo = channel.get(
            "logo",
            ""
        )

        for url, stream_obj in source_items:

            if url in candidates:
                stats["duplicate_urls"] += 1
                continue

            candidates[url] = {
                "url": url,
                "channel": channel,
                "stream": stream_obj,
                "group": group,
                "name": name,
                "id": cid,
                "logo": logo,
            }

    # ========================================================
    # STREAM HEALTH CHECK
    # ========================================================

    print()
    print(
        "----------------------------------"
    )
    print(
        f"UNIQUE STREAM CANDIDATES: {len(candidates)}"
    )
    print(
        "STREAM HEALTH CHECK:"
        + (
            " ENABLED"
            if HEALTH_CHECK
            else " DISABLED"
        )
    )
    print(
        "----------------------------------"
    )

    working = []

    if HEALTH_CHECK and candidates:

        start = time.time()

        with ThreadPoolExecutor(
            max_workers=MAX_WORKERS
        ) as executor:

            future_map = {
                executor.submit(
                    check_stream,
                    item
                ): item
                for item in candidates.values()
            }

            completed = 0
            total = len(
                future_map
            )

            for future in as_completed(
                future_map
            ):

                item = future_map[
                    future
                ]

                try:
                    url, ok, reason = (
                        future.result()
                    )

                except Exception as e:
                    url = item["url"]
                    ok = False
                    reason = str(e)

                completed += 1

                if ok:

                    stats["health_working"] += 1

                    working.append(
                        item
                    )

                else:

                    stats["health_failed"] += 1

                if (
                    completed % 25 == 0
                    or completed == total
                ):
                    print(
                        f"Checked "
                        f"{completed}/{total} | "
                        f"Working "
                        f"{stats['health_working']} | "
                        f"Failed "
                        f"{stats['health_failed']}"
                    )

        elapsed = time.time() - start

        print(
            f"Health check completed in "
            f"{elapsed:.1f}s"
        )

    else:

        working = list(
            candidates.values()
        )

        stats["health_working"] = len(
            working
        )

    # ========================================================
    # SORT
    # ========================================================

    order_map = {
        group: index
        for index, group
        in enumerate(
            GROUP_ORDER
        )
    }

    working.sort(
        key=lambda x: (
            order_map.get(
                x["group"],
                999
            ),
            x["name"].lower(),
            x["url"],
        )
    )

    # ========================================================
    # WRITE M3U
    # ========================================================

    output = [
        "#EXTM3U",
        "#PLAYLIST:Generated IPTV Playlist",
        "",
    ]

    counters = {}

    group_counts = {}

    for item in working:

        group = item["group"]

        display_name = unique_name(
            group,
            item["name"],
            counters
        )

        group_counts[group] = (
            group_counts.get(
                group,
                0
            ) + 1
        )

        output.append(
            make_entry(
                group=group,
                name=display_name,
                channel_id=item["id"],
                logo=item["logo"],
                url=item["url"],
            )
        )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "\n".join(output)
        )

    # ========================================================
    # FINAL STATS
    # ========================================================

    print()
    print(
        "=================================="
    )
    print(
        "PLAYLIST GENERATED"
    )
    print(
        "=================================="
    )

    for group in GROUP_ORDER:

        count = group_counts.get(
            group,
            0
        )

        if count:
            print(
                f"{group}: {count}"
            )

    # Print any extra category that appeared.
    extra_groups = [
        g
        for g in group_counts
        if g not in GROUP_ORDER
    ]

    for group in sorted(
        extra_groups
    ):
        print(
            f"{group}: "
            f"{group_counts[group]}"
        )

    print(
        "----------------------------------"
    )

    total = sum(
        group_counts.values()
    )

    cricket_count = group_counts.get(
        "Sports - Cricket",
        0
    )

    print(
        f"TOTAL WORKING CHANNELS: {total}"
    )

    print(
        f"CRICKET: {cricket_count}"
    )

    print(
        f"Duplicate URLs removed: "
        f"{stats['duplicate_urls']}"
    )

    print(
        f"Regional removed: "
        f"{stats['regional_removed']}"
    )

    print(
        f"Bad channels removed: "
        f"{stats['bad_removed']}"
    )

    print(
        f"No URL: "
        f"{stats['no_url']}"
    )

    print(
        f"Not allowed: "
        f"{stats['not_allowed']}"
    )

    print(
        f"Stream working: "
        f"{stats['health_working']}"
    )

    print(
        f"Stream failed: "
        f"{stats['health_failed']}"
    )

    print(
        "=================================="
    )

    print(
        f"FILE: {OUTPUT_FILE}"
    )

    print(
        "=================================="
    )


# ============================================================
# MAIN
# ============================================================

def main():

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
            f"ERROR FETCHING API: {e}"
        )

        sys.exit(1)

    if not isinstance(
        channels,
        list
    ):
        print(
            "ERROR: channels.json invalid"
        )
        sys.exit(1)

    if not isinstance(
        feeds,
        list
    ):
        print(
            "ERROR: feeds.json invalid"
        )
        sys.exit(1)

    if not isinstance(
        streams,
        list
    ):
        print(
            "ERROR: streams.json invalid"
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

    build_playlist(
        channels,
        feeds,
        streams
    )


if __name__ == "__main__":
    main()
