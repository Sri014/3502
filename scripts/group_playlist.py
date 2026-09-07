#!/usr/bin/env python3

import json
import re
import time
from urllib.parse import quote
from urllib.request import Request, urlopen


# ============================================================
# CONFIG
# ============================================================

CHANNELS_URL = "https://iptv-org.github.io/api/channels.json"
FEEDS_URL = "https://iptv-org.github.io/api/feeds.json"
STREAMS_URL = "https://iptv-org.github.io/api/streams.json"

OUTPUT_FILE = "playlist.m3u"

USER_AGENT = (
    "Mozilla/5.0 (Linux; Android 10) "
    "AppleWebKit/537.36 Chrome/151.0 Safari/537.36"
)

REQUEST_TIMEOUT = 30


# ============================================================
# GROUP ORDER
# ============================================================

GROUP_ORDER = [
    "India - Hindi",
    "India - English",
    "India - Bhojpuri",

    "India - Music",
    "India - News",
    "India - Lifestyle",
    "India - Infotainment",
    "India - Science",
    "India - Kids",
    "India - Entertainment",

    "UK - Hindi",
    "USA - Hindi",
    "Canada - Hindi",
    "Middle East - Hindi",

    "Sports - Cricket",

    "Radio - Hindi",
]


# ============================================================
# LANGUAGE ALIASES
# ============================================================

LANG_ALIASES = {
    "Hindi": {
        "hindi",
        "hin",
    },

    "English": {
        "english",
        "eng",
    },

    "Bhojpuri": {
        "bhojpuri",
        "bho",
    },
}


# ============================================================
# INDIA CATEGORY MAP
# ============================================================

INDIA_CATEGORY_MAP = {
    "music": "India - Music",
    "news": "India - News",
    "lifestyle": "India - Lifestyle",
    "infotainment": "India - Infotainment",
    "science": "India - Science",
    "kids": "India - Kids",
    "entertainment": "India - Entertainment",
}


# ============================================================
# EXCLUSIONS
#
# Handles:
# eVidya
# E-Vidya
# PM eVidya
# PM-E-Vidya
# Swayam Prabha
# Swayam-Prabha
# Vande Gujarat
# Vande-Gujarat
# ============================================================

EXCLUDED_NAME_WORDS = (
    "evidya",
    "pmevidya",
    "swayamprabha",
    "vandegujarat",
)


# ============================================================
# FOREIGN HINDI CHANNELS
# ============================================================

FOREIGN_HINDI_PATTERNS = [

    # COLORS
    r"^colors$",
    r"^colors cineplex$",
    r"^colors cineplex hd$",
    r"^colors rishtey$",

    # SONY
    r"^sony sab$",
    r"^sony sab hd$",
    r"^sony max$",
    r"^sony max hd$",
    r"^sony max 2$",
    r"^sony entertainment television$",
    r"^sony entertainment television hd$",
    r"^sony pal$",

    # ZEE
    r"^zee tv$",
    r"^zee tv hd$",
    r"^zee cinema$",
    r"^zee cinema hd$",
    r"^zee anmol$",
    r"^zee anmol cinema$",
    r"^zee zindagi$",
    r"^zee classic$",

    # STAR
    r"^star plus$",
    r"^star plus hd$",
    r"^star bharat$",
    r"^star bharat hd$",
    r"^star gold$",
    r"^star gold hd$",
    r"^star gold 2$",
    r"^star utsav$",
    r"^star utsav hd$",
    r"^utsav plus$",
    r"^utsav bharat$",
]


# ============================================================
# CRICKET KEYWORDS
#
# Used as fallback in addition to feeds.json detection.
# ============================================================

CRICKET_WORDS = (
    "cricket",
    "willow cricket",
    "fox cricket",
    "sky sports cricket",
    "supersport cricket",
    "ten cricket",
    "t sports cricket",
    "icc cricket",
    "ipl",
    "bcci",
    "big bash",
    "bbl",
    "psl",
    "wpl",
    "cpl",
    "test cricket",
    "county cricket",
    "the hundred",
)


# ============================================================
# HTTP
# ============================================================

def http_get(url):

    req = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "*/*",
        },
    )

    with urlopen(
        req,
        timeout=REQUEST_TIMEOUT
    ) as response:

        return response.read().decode(
            "utf-8",
            errors="replace"
        )


def fetch_json(url):

    print("FETCH:", url)

    data = http_get(url)

    obj = json.loads(data)

    print(
        "OK:",
        len(data),
        "bytes"
    )

    return obj


# ============================================================
# NORMALIZATION
# ============================================================

def text(value):

    if value is None:
        return ""

    return str(value).strip()


def norm(value):

    return re.sub(
        r"\s+",
        " ",
        text(value).lower()
    ).strip()


def normalize_list(value):

    if not value:
        return []

    if isinstance(value, str):
        return [value]

    if isinstance(value, list):
        return value

    return [value]


def normalize_languages(value):

    return {
        norm(x)
        for x in normalize_list(value)
        if norm(x)
    }


# ============================================================
# LANGUAGE
# ============================================================

def get_channel_languages(
    channel,
    feed=None
):

    languages = set()

    # Feed language has priority
    if feed:

        languages.update(
            normalize_languages(
                feed.get("languages")
            )
        )

    # Channel fallback
    languages.update(
        normalize_languages(
            channel.get("languages")
        )
    )

    return languages


def has_language(
    channel,
    feed,
    wanted
):

    languages = get_channel_languages(
        channel,
        feed
    )

    return bool(
        languages &
        LANG_ALIASES[wanted]
    )


# ============================================================
# BUILD HINDI IDS FROM FEEDS
#
# Uses exactly the logic requested:
# languages = hindi / hin
# ============================================================

def build_hindi_channel_ids(feeds):

    ids = set()

    for item in feeds:

        languages = item.get(
            "languages"
        ) or []

        if isinstance(
            languages,
            str
        ):
            languages = [
                languages
            ]

        language_set = {
            norm(x)
            for x in languages
            if norm(x)
        }

        if not (
            language_set &
            {"hindi", "hin"}
        ):
            continue

        channel_id = text(
            item.get("channel")
        )

        if channel_id:
            ids.add(channel_id)

    return ids


# ============================================================
# BUILD GLOBAL CRICKET IDS FROM FEEDS
#
# IMPORTANT:
# No India-country restriction.
# ============================================================

def build_cricket_channel_ids(feeds):

    ids = set()

    for item in feeds:

        values = []

        for key in (
            "name",
            "title",
            "channel",
            "category",
            "description",
            "network",
        ):

            value = item.get(key)

            if isinstance(
                value,
                list
            ):

                values.extend(
                    text(x)
                    for x in value
                )

            else:

                values.append(
                    text(value)
                )

        languages = item.get(
            "languages"
        ) or []

        if isinstance(
            languages,
            list
        ):

            values.extend(
                text(x)
                for x in languages
            )

        else:

            values.append(
                text(languages)
            )

        combined = norm(
            " ".join(
                x for x in values
                if x
            )
        )

        # Feed explicitly mentions cricket
        if "cricket" in combined:

            channel_id = text(
                item.get("channel")
            )

            if channel_id:
                ids.add(channel_id)

    return ids


# ============================================================
# COUNTRY
# ============================================================

def get_country(channel):

    country = channel.get(
        "country",
        ""
    )

    if isinstance(
        country,
        list
    ):

        if country:
            return norm(
                country[0]
            ).upper()

        return ""

    return norm(
        country
    ).upper()


# ============================================================
# CATEGORIES
# ============================================================

def get_categories(channel):

    values = channel.get(
        "categories"
    ) or []

    if isinstance(
        values,
        str
    ):
        values = [
            values
        ]

    return {
        norm(x)
        for x in values
        if norm(x)
    }


# ============================================================
# CHANNEL NAME
# ============================================================

def get_channel_name(
    channel,
    stream=None
):

    if stream:

        title = text(
            stream.get("title")
        )

        if title:
            return title

    name = text(
        channel.get("name")
    )

    if name:
        return name

    alt = channel.get(
        "alt_names"
    ) or []

    if isinstance(
        alt,
        list
    ) and alt:

        return text(
            alt[0]
        )

    return "Unknown Channel"


# ============================================================
# COMBINED TEXT
# ============================================================

def combined_text(
    channel,
    feed=None,
    stream=None
):

    values = []

    for obj in (
        channel,
        feed,
        stream
    ):

        if not obj:
            continue

        for key in (
            "name",
            "title",
            "network",
            "alt_names",
            "description",
            "category",
            "categories",
            "tags",
        ):

            value = obj.get(key)

            if isinstance(
                value,
                list
            ):

                values.extend(
                    text(x)
                    for x in value
                )

            else:

                values.append(
                    text(value)
                )

    return norm(
        " ".join(
            x for x in values
            if x
        )
    )


# ============================================================
# EXCLUSIONS
# ============================================================

def is_excluded(
    channel,
    feed=None,
    stream=None
):

    full_text = combined_text(
        channel,
        feed,
        stream
    )

    compact = re.sub(
        r"[^a-z0-9]",
        "",
        full_text
    )

    return any(
        bad in compact
        for bad in EXCLUDED_NAME_WORDS
    )


# ============================================================
# FOREIGN HINDI
# ============================================================

FOREIGN_HINDI_REGEX = [
    re.compile(
        pattern,
        re.IGNORECASE
    )
    for pattern in FOREIGN_HINDI_PATTERNS
]


def is_verified_foreign_hindi(
    channel,
    feed,
    stream
):

    if not has_language(
        channel,
        feed,
        "Hindi"
    ):
        return False

    name = norm(
        get_channel_name(
            channel,
            stream
        )
    )

    network = norm(
        channel.get("network")
    )

    candidates = [
        name,
        network,
    ]

    for candidate in candidates:

        if not candidate:
            continue

        for pattern in FOREIGN_HINDI_REGEX:

            if pattern.fullmatch(
                candidate
            ):
                return True

    return False


# ============================================================
# INDIA LANGUAGE GROUP
# ============================================================

def get_india_language_group(
    channel,
    feed
):

    if has_language(
        channel,
        feed,
        "Hindi"
    ):
        return "India - Hindi"

    if has_language(
        channel,
        feed,
        "English"
    ):
        return "India - English"

    if has_language(
        channel,
        feed,
        "Bhojpuri"
    ):
        return "India - Bhojpuri"

    return None


# ============================================================
# INDIA CATEGORY GROUP
# ============================================================

def get_india_category_group(
    channel
):

    categories = get_categories(
        channel
    )

    for category, group in (
        INDIA_CATEGORY_MAP.items()
    ):

        if category in categories:
            return group

    return None


# ============================================================
# CRICKET
#
# Global:
# No country restriction.
# ============================================================

def is_cricket(
    channel,
    feed=None,
    stream=None,
    cricket_ids=None
):

    channel_id = text(
        channel.get("id")
    )

    # Primary detection:
    # feeds.json
    if (
        cricket_ids and
        channel_id in cricket_ids
    ):
        return True

    # Fallback detection:
    # channel/feed/stream text
    full_text = combined_text(
        channel,
        feed,
        stream
    )

    for keyword in CRICKET_WORDS:

        if keyword in full_text:
            return True

    return False


# ============================================================
# FOREIGN COUNTRY
# ============================================================

def get_foreign_group(
    channel,
    feed,
    stream
):

    country = get_country(
        channel
    )

    if country == "GB":

        group = "UK - Hindi"

    elif country == "US":

        group = "USA - Hindi"

    elif country == "CA":

        group = "Canada - Hindi"

    elif country in {
        "AE",
        "QA",
        "SA",
        "BH",
        "KW",
        "OM",
    }:

        group = "Middle East - Hindi"

    else:

        return None

    if is_verified_foreign_hindi(
        channel,
        feed,
        stream
    ):
        return group

    return None


# ============================================================
# FEED INDEX
# ============================================================

def build_feed_index(
    feeds
):

    index = {}

    for feed in feeds:

        channel_id = text(
            feed.get("channel")
        )

        feed_id = text(
            feed.get("id")
        )

        if (
            channel_id and
            feed_id
        ):

            index[
                (
                    channel_id,
                    feed_id
                )
            ] = feed

    return index


# ============================================================
# CHANNEL INDEX
# ============================================================

def build_channel_index(
    channels
):

    result = {}

    for channel in channels:

        cid = text(
            channel.get("id")
        )

        if cid:
            result[cid] = channel

    return result


# ============================================================
# STREAM URL
# ============================================================

def get_stream_url(
    stream
):

    return text(
        stream.get("url")
    )


# ============================================================
# M3U TEXT
# ============================================================

def clean_m3u_text(
    value
):

    value = text(
        value
    )

    value = value.replace(
        '"',
        "'"
    )

    value = value.replace(
        "\r",
        " "
    )

    value = value.replace(
        "\n",
        " "
    )

    return value.strip()


# ============================================================
# EXTINF
# ============================================================

def make_extinf(
    group,
    name,
    channel,
    stream
):

    channel_id = clean_m3u_text(
        channel.get("id")
    )

    logo = clean_m3u_text(
        channel.get("logo")
    )

    if not logo:

        logo = clean_m3u_text(
            stream.get("logo")
        )

    tvg_id = channel_id

    parts = [
        "#EXTINF:-1",
        f'tvg-id="{tvg_id}"',
        f'tvg-name="{clean_m3u_text(name)}"',
    ]

    if logo:

        parts.append(
            f'tvg-logo="{logo}"'
        )

    parts.append(
        f'group-title="{group}"'
    )

    parts.append(
        f",{clean_m3u_text(name)}"
    )

    return " ".join(parts)


# ============================================================
# M3U ENTRY
# ============================================================

def make_entry(
    group,
    channel,
    feed,
    stream
):

    url = get_stream_url(
        stream
    )

    if not url:
        return None

    name = get_channel_name(
        channel,
        stream
    )

    lines = [
        make_extinf(
            group,
            name,
            channel,
            stream
        )
    ]

    referrer = text(
        stream.get("referrer")
    )

    user_agent = text(
        stream.get("user_agent")
    )

    if referrer:

        lines.append(
            "#EXTVLCOPT:http-referrer="
            + referrer
        )

    if user_agent:

        lines.append(
            "#EXTVLCOPT:http-user-agent="
            + user_agent
        )

    lines.append(
        url
    )

    return "\n".join(
        lines
    )


# ============================================================
# RADIO GARDEN
# ============================================================

RADIO_SEARCHES = [
    "Hindi",
    "Hindi Radio",
    "Hindi FM",
    "Hindi Music",
    "Bollywood",
]


def recursive_objects(obj):

    if isinstance(
        obj,
        dict
    ):

        yield obj

        for value in obj.values():

            yield from recursive_objects(
                value
            )

    elif isinstance(
        obj,
        list
    ):

        for value in obj:

            yield from recursive_objects(
                value
            )


def extract_ids(obj):

    ids = set()

    for item in recursive_objects(
        obj
    ):

        if not isinstance(
            item,
            dict
        ):
            continue

        for key in (
            "id",
            "channelId",
            "channel_id",
        ):

            value = item.get(
                key
            )

            if value is None:
                continue

            value = text(
                value
            )

            if value:
                ids.add(
                    value
                )

    return ids


def radio_garden_search(
    query
):

    url = (
        "https://radio.garden/api/search?q="
        + quote(query)
    )

    try:

        return fetch_json(
            url
        )

    except Exception as e:

        print(
            "Radio Garden search failed:",
            query,
            e
        )

        return None


def get_radio_channel(
    channel_id
):

    url = (
        "https://radio.garden/api/"
        "ara/content/channel/"
        + quote(channel_id)
    )

    try:

        return fetch_json(
            url
        )

    except Exception as e:

        print(
            "Radio Garden channel failed:",
            channel_id,
            e
        )

        return None


def is_hindi_radio(
    data
):

    if not data:
        return False

    words = []

    for item in recursive_objects(
        data
    ):

        if not isinstance(
            item,
            dict
        ):
            continue

        for key in (
            "name",
            "title",
            "description",
            "genre",
            "language",
            "languages",
            "tags",
        ):

            value = item.get(
                key
            )

            if isinstance(
                value,
                list
            ):

                words.extend(
                    text(x)
                    for x in value
                )

            else:

                words.append(
                    text(value)
                )

    combined = norm(
        " ".join(
            x for x in words
            if x
        )
    )

    hindi_words = [
        "hindi",
        "hindustani",
        "bollywood",
        "hindi fm",
        "hindi radio",
    ]

    return any(
        word in combined
        for word in hindi_words
    )


def build_radio_entries():

    entries = []

    seen_radio_ids = set()

    for query in RADIO_SEARCHES:

        result = radio_garden_search(
            query
        )

        if not result:
            continue

        ids = extract_ids(
            result
        )

        print(
            "Radio Garden:",
            query,
            "IDs:",
            len(ids)
        )

        for channel_id in ids:

            if channel_id in seen_radio_ids:
                continue

            seen_radio_ids.add(
                channel_id
            )

            details = get_radio_channel(
                channel_id
            )

            if not details:
                continue

            if not is_hindi_radio(
                details
            ):
                continue

            name = None

            for item in recursive_objects(
                details
            ):

                if not isinstance(
                    item,
                    dict
                ):
                    continue

                for key in (
                    "name",
                    "title",
                ):

                    value = text(
                        item.get(key)
                    )

                    if value:

                        name = value
                        break

                if name:
                    break

            if not name:

                name = (
                    "Hindi Radio "
                    + channel_id
                )

            stream_url = (
                "https://radio.garden/api/"
                "ara/content/listen/"
                + quote(channel_id)
                + "/channel.mp3"
            )

            entries.append({
                "name": name,
                "url": stream_url,
            })

            time.sleep(
                0.1
            )

    return entries


# ============================================================
# MAIN PLAYLIST BUILDER
# ============================================================

def build_playlist():

    print()
    print("========================================")
    print(" IPTV PLAYLIST BUILDER")
    print("========================================")
    print()

    # --------------------------------------------------------
    # FETCH IPTV DATA
    # --------------------------------------------------------

    channels_data = fetch_json(
        CHANNELS_URL
    )

    feeds_data = fetch_json(
        FEEDS_URL
    )

    streams_data = fetch_json(
        STREAMS_URL
    )

    if not isinstance(
        channels_data,
        list
    ):

        raise RuntimeError(
            "channels.json invalid"
        )

    if not isinstance(
        feeds_data,
        list
    ):

        raise RuntimeError(
            "feeds.json invalid"
        )

    if not isinstance(
        streams_data,
        list
    ):

        raise RuntimeError(
            "streams.json invalid"
        )

    channels = build_channel_index(
        channels_data
    )

    feed_index = build_feed_index(
        feeds_data
    )

    # --------------------------------------------------------
    # BUILD SPECIAL INDEXES
    # --------------------------------------------------------

    hindi_ids = build_hindi_channel_ids(
        feeds_data
    )

    cricket_ids = build_cricket_channel_ids(
        feeds_data
    )

    print()
    print(
        "CHANNELS:",
        len(channels)
    )

    print(
        "FEEDS:",
        len(feeds_data)
    )

    print(
        "STREAMS:",
        len(streams_data)
    )

    print(
        "HINDI FEED CHANNEL IDS:",
        len(hindi_ids)
    )

    print(
        "CRICKET FEED CHANNEL IDS:",
        len(cricket_ids)
    )

    # --------------------------------------------------------
    # GROUP STORAGE
    # --------------------------------------------------------

    groups = {
        group: []
        for group in GROUP_ORDER
    }

    # --------------------------------------------------------
    # GLOBAL URL DEDUP
    # --------------------------------------------------------

    seen_urls = set()

    # --------------------------------------------------------
    # PROCESS STREAMS
    # --------------------------------------------------------

    processed = 0
    skipped = 0

    for stream in streams_data:

        url = get_stream_url(
            stream
        )

        if not url:

            skipped += 1
            continue

        # Exact same URL globally
        if url in seen_urls:

            skipped += 1
            continue

        channel_id = text(
            stream.get("channel")
        )

        if not channel_id:

            skipped += 1
            continue

        channel = channels.get(
            channel_id
        )

        if not channel:

            skipped += 1
            continue

        feed_id = text(
            stream.get("feed")
        )

        feed = feed_index.get(
            (
                channel_id,
                feed_id
            )
        )

        # ----------------------------------------------------
        # EXCLUDE eVidya / Swayam Prabha / Vande Gujarat
        # ----------------------------------------------------

        if is_excluded(
            channel,
            feed,
            stream
        ):

            skipped += 1
            continue

        country = get_country(
            channel
        )

        group = None

        # ====================================================
        # INDIA
        # ====================================================

        if country == "IN":

            # ------------------------------------------------
            # HINDI FEED IDS FIRST
            # ------------------------------------------------

            if channel_id in hindi_ids:

                group = "India - Hindi"

            else:

                group = get_india_language_group(
                    channel,
                    feed
                )

            # ------------------------------------------------
            # CATEGORY GROUP
            # ------------------------------------------------

            if group is None:

                group = get_india_category_group(
                    channel
                )

        # ====================================================
        # FOREIGN HINDI
        # ====================================================

        if group is None:

            group = get_foreign_group(
                channel,
                feed,
                stream
            )

        # ====================================================
        # GLOBAL CRICKET
        #
        # No country restriction.
        # ====================================================

        if group is None:

            if is_cricket(
                channel,
                feed,
                stream,
                cricket_ids
            ):

                group = "Sports - Cricket"

        # ====================================================
        # NOTHING MATCHED
        # ====================================================

        if group is None:

            skipped += 1
            continue

        # ----------------------------------------------------
        # CREATE M3U ENTRY
        # ----------------------------------------------------

        entry = make_entry(
            group,
            channel,
            feed,
            stream
        )

        if not entry:

            skipped += 1
            continue

        # Mark URL used
        seen_urls.add(
            url
        )

        groups[group].append(
            entry
        )

        processed += 1

    # ========================================================
    # RADIO GARDEN
    # ========================================================

    print()
    print("========================================")
    print(" RADIO GARDEN")
    print("========================================")

    radio_entries = build_radio_entries()

    radio_seen = set()

    for radio in radio_entries:

        url = radio["url"]

        if url in seen_urls:
            continue

        if url in radio_seen:
            continue

        radio_seen.add(
            url
        )

        seen_urls.add(
            url
        )

        name = clean_m3u_text(
            radio["name"]
        )

        entry = (
            '#EXTINF:-1 '
            'group-title="Radio - Hindi",'
            + name
            + "\n"
            + url
        )

        groups[
            "Radio - Hindi"
        ].append(
            entry
        )

    # ========================================================
    # WRITE PLAYLIST
    # ========================================================

    output = [
        "#EXTM3U"
    ]

    for group in GROUP_ORDER:

        for entry in groups[group]:

            output.append(
                entry
            )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "\n".join(output)
            + "\n"
        )

    # ========================================================
    # FINAL COUNTS + CHANNEL NAMES
    # ========================================================

    print()
    print("========================================")
    print(" FINAL PLAYLIST")
    print(" CHANNEL NAMES + COUNTS")
    print("========================================")

    total = 0

    for group in GROUP_ORDER:

        entries = groups[group]

        count = len(
            entries
        )

        total += count

        print()
        print(
            f"### {group} ({count})"
        )

        print(
            "----------------------------------------"
        )

        for i, entry in enumerate(
            entries,
            1
        ):

            extinf = (
                entry.splitlines()[0]
                if entry
                else ""
            )

            if "," in extinf:

                name = (
                    extinf.split(
                        ",",
                        1
                    )[1].strip()
                )

            else:

                name = "Unknown"

            print(
                f"{i}. {name}"
            )

    # ========================================================
    # SUMMARY
    # ========================================================

    print()
    print("========================================")
    print(" FINAL SUMMARY")
    print("========================================")

    for group in GROUP_ORDER:

        print(
            f"{group:<30} "
            f"{len(groups[group])}"
        )

    print("----------------------------------------")

    print(
        f"{'TOTAL CHANNELS':<30}"
        f"{total}"
    )

    print(
        f"{'PROCESSED':<30}"
        f"{processed}"
    )

    print(
        f"{'UNMATCHED/SKIPPED':<30}"
        f"{skipped}"
    )

    print(
        f"{'UNIQUE URLS':<30}"
        f"{len(seen_urls)}"
    )

    print("----------------------------------------")

    print(
        "OUTPUT:",
        OUTPUT_FILE
    )

    print("========================================")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    try:

        build_playlist()

    except KeyboardInterrupt:

        print()
        print("Stopped.")

    except Exception as e:

        print()
        print(
            "ERROR:",
            repr(e)
        )

        raise
