import json
import re
import time
from urllib.parse import quote
from urllib.request import Request, urlopen

CHANNELS_URL = "https://iptv-org.github.io/api/channels.json"
FEEDS_URL = "https://iptv-org.github.io/api/feeds.json"
STREAMS_URL = "https://iptv-org.github.io/api/streams.json"

OUTPUT_FILE = "playlist.m3u"

GROUP_ORDER = [
    "India - Hindi",
    "India - English",
    "India - Bhojpuri",
    "UK - Hindi",
    "USA - Hindi",
    "Canada - Hindi",
    "Middle East - Hindi",
    "Sports - Cricket",
    "Radio - Hindi",
]

HINDI = {"hindi", "hin"}
ENGLISH = {"english", "eng"}
BHOJPURI = {"bhojpuri", "bho"}

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

BAD_WORDS = (
    "evidya",
    "pmevidya",
    "swayamprabha",
    "vandegujarat",
)

# STRICT cricket channel names.
# Cricket word in description/feed/network alone is NOT enough.
CRICKET_NAMES = {
    "cricket gold",
    "psl tv",
    "sky sports cricket",
    "willow",
    "willow sports",
    "wplg 10.1",
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


def text(value):
    if value is None:
        return ""

    if isinstance(value, list):
        return " ".join(text(x) for x in value)

    if isinstance(value, dict):
        return " ".join(text(x) for x in value.values())

    return str(value)


def norm(value):
    return text(value).strip().lower()


def get_json(url):
    req = Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urlopen(req, timeout=90) as response:
        return json.load(response)


def get_languages(obj):
    if not obj:
        return set()

    value = obj.get("languages") or []

    if isinstance(value, str):
        value = [value]

    return {
        norm(x)
        for x in value
        if norm(x)
    }


def get_country(obj):
    if not obj:
        return set()

    value = obj.get("country")

    if isinstance(value, list):
        return {
            norm(x).upper()
            for x in value
            if norm(x)
        }

    if value:
        return {norm(value).upper()}

    return set()


def get_name(channel, stream=None):
    # Always prefer canonical channel name.
    name = text(channel.get("name")).strip()

    if name:
        return name

    if stream:
        name = text(stream.get("title")).strip()

        if name:
            return name

    alt = channel.get("alt_names") or []

    if isinstance(alt, list) and alt:
        return text(alt[0]).strip()

    return "Unknown"


def get_stream_url(stream):
    for key in (
        "url",
        "stream",
        "src",
        "hls",
    ):
        value = stream.get(key)

        if isinstance(value, str) and value.strip():
            return value.strip()

    return ""


def combined_text(channel, feeds, stream):
    values = []

    objects = [channel]

    if feeds:
        if not isinstance(feeds, list):
            feeds = [feeds]

        objects.extend(feeds)

    if stream:
        objects.append(stream)

    for obj in objects:
        if not obj:
            continue

        for key in (
            "name",
            "title",
            "network",
            "description",
            "category",
            "categories",
            "tags",
            "alt_names",
        ):
            if key in obj:
                values.append(text(obj.get(key)))

    return " ".join(values).lower()


def is_bad(channel, feeds, stream):
    value = re.sub(
        r"[^a-z0-9]",
        "",
        combined_text(channel, feeds, stream)
    )

    return any(word in value for word in BAD_WORDS)


def has_regional_language(channel, feeds):
    langs = get_languages(channel)

    if feeds:
        if not isinstance(feeds, list):
            feeds = [feeds]

        for feed in feeds:
            langs |= get_languages(feed)

    return bool(langs & REGIONAL)


def has_hindi(channel, feeds):
    if get_languages(channel) & HINDI:
        return True

    if feeds:
        if not isinstance(feeds, list):
            feeds = [feeds]

        for feed in feeds:
            if get_languages(feed) & HINDI:
                return True

    return False


def has_english(channel, feeds):
    if get_languages(channel) & ENGLISH:
        return True

    if feeds:
        if not isinstance(feeds, list):
            feeds = [feeds]

        for feed in feeds:
            if get_languages(feed) & ENGLISH:
                return True

    return False


def has_bhojpuri(channel, feeds):
    if get_languages(channel) & BHOJPURI:
        return True

    if feeds:
        if not isinstance(feeds, list):
            feeds = [feeds]

        for feed in feeds:
            if get_languages(feed) & BHOJPURI:
                return True

    return False


def cricket_channel(channel):
    name = norm(channel.get("name"))

    return name in CRICKET_NAMES


def make_entry(group, channel, stream, display_name):
    url = get_stream_url(stream)

    logo = text(channel.get("logo")).strip()

    lines = [
        f'#EXTINF:-1 tvg-id="{text(channel.get("id"))}" '
        f'tvg-name="{display_name}" '
        f'tvg-logo="{logo}" '
        f'group-title="{group}",{display_name}'
    ]

    lines.append(url)

    return "\n".join(lines)


def build_feed_index(feeds):
    index = {}

    for feed in feeds:
        cid = text(feed.get("channel"))

        if not cid:
            continue

        index.setdefault(cid, []).append(feed)

    return index


def build_channel_index(channels):
    return {
        text(channel.get("id")): channel
        for channel in channels
        if text(channel.get("id"))
    }


def build_hindi_ids(feeds):
    ids = set()

    for feed in feeds:
        cid = text(feed.get("channel"))

        if not cid:
            continue

        if get_languages(feed) & HINDI:
            ids.add(cid)

    return ids


def unique_name(group, base_name, counters):
    key = (
        group,
        norm(base_name)
    )

    counters[key] = counters.get(key, 0) + 1

    number = counters[key]

    if number == 1:
        return base_name

    return f"{base_name} {number}"


def build_playlist():
    print("Downloading channels.json...")
    channels = get_json(CHANNELS_URL)

    print("Downloading feeds.json...")
    feeds = get_json(FEEDS_URL)

    print("Downloading streams.json...")
    streams = get_json(STREAMS_URL)

    channel_index = build_channel_index(channels)
    feed_index = build_feed_index(feeds)
    hindi_ids = build_hindi_ids(feeds)

    grouped = {
        group: []
        for group in GROUP_ORDER
    }

    # IMPORTANT:
    # One URL globally = one entry only.
    seen_urls = set()

    # Different URLs for same channel = Name 2/3...
    name_counters = {}

    stats = {
        "total_streams": 0,
        "accepted": 0,
        "duplicate_urls": 0,
        "regional_removed": 0,
        "bad_removed": 0,
        "not_allowed": 0,
        "no_url": 0,
    }

    for stream in streams:
        stats["total_streams"] += 1

        cid = text(stream.get("channel"))

        if not cid:
            continue

        channel = channel_index.get(cid)

        if not channel:
            continue

        url = get_stream_url(stream)

        if not url:
            stats["no_url"] += 1
            continue

        # SAME EXACT STREAM URL:
        # remove before name numbering.
        if url in seen_urls:
            stats["duplicate_urls"] += 1
            continue

        channel_feeds = feed_index.get(cid, [])

        if not channel_feeds:
            channel_feeds = [None]

        if is_bad(
            channel,
            channel_feeds,
            stream
        ):
            stats["bad_removed"] += 1
            continue

        countries = get_country(channel)

        group = None

        # ==================================================
        # INDIA
        # ONLY Hindi / English / Bhojpuri
        # ==================================================

        if "IN" in countries:

            # Absolutely reject Indian regional languages.
            if has_regional_language(
                channel,
                channel_feeds
            ):
                stats["regional_removed"] += 1
                continue

            if (
                cid in hindi_ids
                or has_hindi(channel, channel_feeds)
            ):
                group = "India - Hindi"

            elif has_english(
                channel,
                channel_feeds
            ):
                group = "India - English"

            elif has_bhojpuri(
                channel,
                channel_feeds
            ):
                group = "India - Bhojpuri"

            else:
                # NO fallback categories.
                stats["not_allowed"] += 1
                continue

        # ==================================================
        # FOREIGN HINDI
        # ==================================================

        else:
            for country_code, foreign_group in FOREIGN_COUNTRIES.items():

                if country_code not in countries:
                    continue

                if (
                    cid in hindi_ids
                    or has_hindi(channel, channel_feeds)
                ):
                    group = foreign_group

                break

            # ==================================================
            # STRICT GLOBAL CRICKET
            # ==================================================

            if group is None and cricket_channel(channel):
                group = "Sports - Cricket"

        if group is None:
            stats["not_allowed"] += 1
            continue

        # ==================================================
        # ACCEPT
        # ==================================================

        seen_urls.add(url)

        base_name = get_name(
            channel,
            stream
        )

        display_name = unique_name(
            group,
            base_name,
            name_counters
        )

        grouped[group].append(
            make_entry(
                group,
                channel,
                stream,
                display_name
            )
        )

        stats["accepted"] += 1

    # ======================================================
    # WRITE PLAYLIST
    # ======================================================

    output = [
        "#EXTM3U"
    ]

    for group in GROUP_ORDER:
        output.extend(grouped[group])

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(
            "\n".join(output) + "\n"
        )

    # ======================================================
    # FINAL COUNTS
    # ======================================================

    print()
    print("========== FINAL RESULT ==========")

    for group in GROUP_ORDER:
        print(
            f"{group}: "
            f"{len(grouped[group])}"
        )

    print("----------------------------------")

    total = sum(
        len(grouped[group])
        for group in GROUP_ORDER
    )

    cricket_total = len(
        grouped["Sports - Cricket"]
    )

    print(
        "TOTAL UNIQUE CHANNELS:",
        total
    )

    print(
        "CRICKET:",
        cricket_total
    )

    print("----------------------------------")

    print(
        "Duplicate streams removed:",
        stats["duplicate_urls"]
    )

    print(
        "Regional removed:",
        stats["regional_removed"]
    )

    print(
        "Bad channels removed:",
        stats["bad_removed"]
    )

    print(
        "No URL:",
        stats["no_url"]
    )

    print(
        "Not allowed:",
        stats["not_allowed"]
    )

    print("----------------------------------")
    print(
        "Playlist:",
        OUTPUT_FILE
    )
    print("==================================")


if __name__ == "__main__":
    build_playlist()
