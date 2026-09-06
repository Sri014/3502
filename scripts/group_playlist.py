#!/usr/bin/env python3

import argparse
import re
from pathlib import Path
from urllib.parse import urlparse


# ============================================================
# FINAL GROUPS
# ============================================================

ALLOWED_CATEGORIES = {
    "News",
    "Entertainment",
    "Movies",
    "Music",
    "Kids",
    "Infotainment",
    "Science",
    "Lifestyle",
    "Business",
    "Sports",
}

EXCLUDED_GROUPS = {
    "regional",
    "devotional",
    "education",
    "spiritual",
}


# ============================================================
# CHANNEL CATEGORY MAP
# ============================================================

CHANNEL_MAP = {

    # ---------------- NEWS ----------------
    "aaj tak": "News",
    "aajtak": "News",
    "india today": "News",
    "ndtv india": "News",
    "ndtv": "News",
    "news18 india": "News",
    "news18": "News",
    "zee news": "News",
    "zee business": "Business",
    "times now": "News",
    "times now navbharat": "News",
    "republic tv": "News",
    "republic bharat": "News",
    "tv9 bharatvarsh": "News",
    "tv9 telugu": "News",
    "tv9 kannada": "News",
    "abp news": "News",
    "abp ananda": "News",
    "abp asmita": "News",
    "abp majha": "News",
    "abp ganga": "News",
    "news24": "News",
    "india news": "News",
    "good news today": "News",
    "bharat express": "News",
    "firstpost": "News",
    "the lallantop": "News",
    "wion": "News",

    # ---------------- ENTERTAINMENT ----------------
    "sony sab": "Entertainment",
    "sony pal": "Entertainment",
    "sony entertainment": "Entertainment",
    "sony tv": "Entertainment",
    "sony max": "Movies",
    "sony wah": "Movies",
    "sony max 2": "Movies",
    "sony aath": "Entertainment",

    "star plus": "Entertainment",
    "star utsav": "Entertainment",
    "star bharat": "Entertainment",
    "star pravah": "Entertainment",
    "star jalsha": "Entertainment",
    "star vijay": "Entertainment",
    "star maa": "Entertainment",
    "star suvarna": "Entertainment",
    "star kiran": "Entertainment",
    "star sports": "Sports",

    "colors": "Entertainment",
    "colors hindi": "Entertainment",
    "colors rishtey": "Entertainment",
    "colors cineplex": "Movies",
    "colors cineplex superhits": "Movies",
    "colors bangla": "Entertainment",
    "colors kannada": "Entertainment",
    "colors marathi": "Entertainment",
    "colors gujarati": "Entertainment",
    "colors tamil": "Entertainment",
    "colors odia": "Entertainment",

    "zee tv": "Entertainment",
    "zee anmol": "Entertainment",
    "zee anmol cinema": "Movies",
    "zee cinema": "Movies",
    "zee cinema hd": "Movies",
    "zee classic": "Movies",
    "zee bangla": "Entertainment",
    "zee marathi": "Entertainment",
    "zee kannada": "Entertainment",
    "zee tamil": "Entertainment",
    "zee telugu": "Entertainment",
    "zee sarthak": "Entertainment",
    "zee ganga": "Entertainment",
    "zee zindagi": "Entertainment",

    "sony marathi": "Entertainment",
    "sony yay": "Kids",
    "sony aath": "Entertainment",

    "dangal": "Entertainment",
    "dangal 2": "Entertainment",
    "dangal cinema": "Movies",
    "b4u entertainment": "Entertainment",

    # ---------------- MOVIES ----------------
    "b4u movies": "Movies",
    "b4u cinema": "Movies",
    "b4u kadak": "Movies",
    "mastiii": "Music",
    "goldmines": "Movies",
    "goldmines bollywood": "Movies",
    "goldmines movies": "Movies",
    "bollywood": "Movies",
    "manoranjan tv": "Movies",
    "manoranjan grand": "Movies",
    "wow cinema": "Movies",
    "dhamaal tv": "Movies",
    "filamchi": "Movies",
    "sheemaroo": "Movies",
    "sheemaroo tv": "Movies",
    "sheemaroo umang": "Entertainment",

    # ---------------- MUSIC ----------------
    "b4u music": "Music",
    "9xm": "Music",
    "9x music": "Music",
    "9x jhakaas": "Music",
    "9x tashan": "Music",
    "mtv": "Music",
    "mtv beats": "Music",
    "zing": "Music",
    "zoom": "Music",
    "music india": "Music",
    "mastiii": "Music",
    "songs": "Music",

    # ---------------- KIDS ----------------
    "cartoon network": "Kids",
    "pogo": "Kids",
    "hungama": "Kids",
    "hungama tv": "Kids",
    "discovery kids": "Kids",
    "sony yay": "Kids",
    "nick": "Kids",
    "nick hd+": "Kids",
    "sonic": "Kids",
    "super hungama": "Kids",

    # ---------------- BUSINESS ----------------
    "cnbc tv18": "Business",
    "cnbc awaaz": "Business",
    "cnbc": "Business",
    "ndtv profit": "Business",
    "business today": "Business",
    "zee business": "Business",
    "et now": "Business",
    "et now swadesh": "Business",

    # ---------------- SPORTS ----------------
    "star sports": "Sports",
    "star sports 1": "Sports",
    "star sports 2": "Sports",
    "star sports 3": "Sports",
    "star sports 1 hindi": "Sports",
    "star sports 2 hindi": "Sports",
    "star sports select": "Sports",
    "star sports select 1": "Sports",
    "star sports select 2": "Sports",
    "star sports tamil": "Sports",
    "star sports telugu": "Sports",
    "star sports kannada": "Sports",
    "star sports hindi": "Sports",
    "sony sports": "Sports",
    "sony sports ten 1": "Sports",
    "sony sports ten 2": "Sports",
    "sony sports ten 3": "Sports",
    "sony sports ten 4": "Sports",
    "sony sports ten 5": "Sports",
    "sony ten 1": "Sports",
    "sony ten 2": "Sports",
    "sony ten 3": "Sports",
    "sony ten 4": "Sports",
    "sony ten 5": "Sports",
    "sports18": "Sports",
    "sports18 1": "Sports",
    "sports18 2": "Sports",
    "sports18 khel": "Sports",
    "sports18 hindi": "Sports",
    "dd sports": "Sports",
    "eurosport": "Sports",

    # ---------------- INFOTAINMENT ----------------
    "discovery": "Infotainment",
    "discovery channel": "Infotainment",
    "discovery hd": "Infotainment",
    "animal planet": "Infotainment",
    "history tv": "Infotainment",
    "history tv18": "Infotainment",
    "epic": "Infotainment",
    "epic tv": "Infotainment",
    "travel xp": "Lifestyle",
    "travelxp": "Lifestyle",

    # ---------------- SCIENCE ----------------
    "nat geo": "Science",
    "national geographic": "Science",
    "nat geo hd": "Science",
    "science": "Science",

    # ---------------- LIFESTYLE ----------------
    "food food": "Lifestyle",
    "living foodz": "Lifestyle",
    "fashion tv": "Lifestyle",
    "fbt": "Lifestyle",
    "travel xp": "Lifestyle",
    "travelxp": "Lifestyle",
}


# ============================================================
# LANGUAGE DETECTION
# ============================================================

LANGUAGE_WORDS = {
    "hindi": "Hindi",
    "hin": "Hindi",

    "english": "English",
    "eng": "English",

    "bhojpuri": "Bhojpuri",

    "bengali": "Bengali",
    "bangla": "Bengali",

    "tamil": "Tamil",
    "telugu": "Telugu",
    "kannada": "Kannada",
    "malayalam": "Malayalam",
    "marathi": "Marathi",
    "punjabi": "Punjabi",
    "gujarati": "Gujarati",
    "odia": "Odia",
    "oriya": "Odia",
    "assamese": "Assamese",
}


# ============================================================
# FOREIGN COUNTRY / CHANNEL MARKERS
#
# Non-cricket foreign sources are removed.
# Cricket from these sources is allowed.
# ============================================================

FOREIGN_MARKERS = {
    "uk",
    "united kingdom",
    "britain",
    "england",
    "usa",
    "us",
    "united states",
    "america",
    "australia",
    "new zealand",
    "south africa",
    "pakistan",
    "bangladesh",
    "sri lanka",
    "afghanistan",
    "west indies",
    "ireland",
    "zimbabwe",
    "scotland",
    "wales",
    "canada",
    "uae",
    "united arab emirates",
    "qatar",
    "saudi",
    "singapore",
    "malaysia",
    "nepal",
}


# Explicit international channel names.
# These are rejected unless the stream is Cricket.
FOREIGN_CHANNEL_MARKERS = {
    "bbc news",
    "bbc world",
    "bbc world news",
    "cnn international",
    "cnn international hd",
    "al jazeera",
    "aljazeera",
    "sky news",
    "fox news",
    "france 24",
    "dw english",
    "dw news",
    "euronews",
    "trt world",
    "cgtn",
    "nhk world",
    "abc australia",
    "rt news",
    "rt international",
    "sky sports",
    "bein sports",
    "willow",
}


# ============================================================
# HELPERS
# ============================================================

def clean(value):
    if value is None:
        return ""

    value = str(value)

    value = value.replace("&amp;", "&")
    value = value.replace("&quot;", '"')
    value = value.replace("&#39;", "'")

    value = re.sub(r"\s+", " ", value)

    return value.strip()


def lower(value):
    return clean(value).lower()


def parse_extinf(line):
    attrs = {}

    match = re.match(r"#EXTINF:[^ ]*(?:\s+(.*))?,(.*)$", line)

    if not match:
        return attrs, ""

    attribute_text = match.group(1) or ""
    name = clean(match.group(2))

    pattern = re.compile(r'([\w-]+)="([^"]*)"')

    for key, value in pattern.findall(attribute_text):
        attrs[key.lower()] = clean(value)

    return attrs, name


def get_channel_name(attrs, name):
    for key in (
        "tvg-name",
        "tvg-name",
        "channel-name",
        "name",
    ):
        if attrs.get(key):
            return clean(attrs[key])

    return clean(name)


def find_exact_mapping(name):
    n = lower(name)

    if n in CHANNEL_MAP:
        return CHANNEL_MAP[n]

    # Longest mapping first.
    for key in sorted(CHANNEL_MAP, key=len, reverse=True):
        if key in n:
            return CHANNEL_MAP[key]

    return None


def detect_sport(attrs, name, group, url):
    text = " ".join([
        lower(attrs.get("group-title", "")),
        lower(attrs.get("tvg-name", "")),
        lower(attrs.get("tvg-language", "")),
        lower(name),
        lower(group),
        lower(url),
    ])

    sport_words = (
        "sport",
        "sports",
        "cricket",
        "football",
        "soccer",
        "hockey",
        "tennis",
        "badminton",
        "wwe",
        "kabaddi",
        "basketball",
        "baseball",
        "f1",
        "formula 1",
        "motogp",
        "golf",
        "boxing",
        "wrestling",
    )

    return any(word in text for word in sport_words)


def is_cricket(attrs, name, group, url):
    text = " ".join([
        lower(attrs.get("group-title", "")),
        lower(attrs.get("tvg-name", "")),
        lower(name),
        lower(group),
        lower(url),
    ])

    return "cricket" in text


def detect_language(attrs, name, group):
    explicit = lower(attrs.get("tvg-language", ""))

    if explicit:
        for word, language in LANGUAGE_WORDS.items():
            if word in explicit:
                return language

    text = " ".join([
        lower(name),
        lower(group),
    ])

    for word, language in LANGUAGE_WORDS.items():
        if re.search(r"\b" + re.escape(word) + r"\b", text):
            return language

    return ""


def category_from_old_group(group):
    g = lower(group)

    if not g:
        return None

    if any(x in g for x in EXCLUDED_GROUPS):
        return None

    if g in {
        "news",
        "entertainment",
        "movies",
        "movie",
        "music",
        "kids",
        "infotainment",
        "science",
        "lifestyle",
        "business",
        "sports",
    }:
        mapping = {
            "movie": "Movies",
        }

        return mapping.get(g, g.title())

    return None


def keyword_category(attrs, name, group):
    text = " ".join([
        lower(attrs.get("group-title", "")),
        lower(name),
        lower(group),
    ])

    # Sports gets highest priority.
    if detect_sport(attrs, name, group, ""):
        return "Sports"

    keywords = {
        "news": "News",
        "breaking news": "News",
        "entertainment": "Entertainment",
        "serial": "Entertainment",
        "movie": "Movies",
        "movies": "Movies",
        "cinema": "Movies",
        "music": "Music",
        "kids": "Kids",
        "cartoon": "Kids",
        "business": "Business",
        "finance": "Business",
        "infotainment": "Infotainment",
        "science": "Science",
        "nature": "Science",
        "lifestyle": "Lifestyle",
        "travel": "Lifestyle",
        "food": "Lifestyle",
    }

    for word, category in sorted(
        keywords.items(),
        key=lambda x: len(x[0]),
        reverse=True,
    ):
        if word in text:
            return category

    return None


def classify(attrs, name, url, source_file=""):
    group = attrs.get("group-title", "")

    # Explicitly excluded groups.
    if any(x in lower(group) for x in EXCLUDED_GROUPS):
        return None

    # Sports always goes to one group.
    if detect_sport(attrs, name, group, url):
        return "Sports"

    mapped = find_exact_mapping(name)

    if mapped in ALLOWED_CATEGORIES:
        return mapped

    old_group = category_from_old_group(group)

    if old_group in ALLOWED_CATEGORIES:
        return old_group

    category = keyword_category(attrs, name, group)

    if category in ALLOWED_CATEGORIES:
        return category

    return None


# ============================================================
# FOREIGN FILTER
# ============================================================

def contains_foreign_marker(text):
    text = lower(text)

    for marker in FOREIGN_MARKERS:
        if re.search(r"\b" + re.escape(marker) + r"\b", text):
            return True

    return False


def contains_foreign_channel_marker(text):
    text = lower(text)

    for marker in FOREIGN_CHANNEL_MARKERS:
        if marker in text:
            return True

    return False


def source_is_international(source_file):
    filename = lower(Path(source_file).name)

    markers = (
        "intl",
        "international",
        "foreign",
        "world",
        "global",
    )

    return any(x in filename for x in markers)


def is_indian_or_allowed_cricket(attrs, name, group, url, source_file):
    """
    Final filtering rule:

    Indian channels:
        ALLOW

    Foreign cricket:
        ALLOW

    Foreign non-cricket:
        REMOVE
    """

    cricket = is_cricket(attrs, name, group, url)

    # Cricket from any country is allowed.
    if cricket:
        return True

    text = " ".join([
        lower(attrs.get("tvg-country", "")),
        lower(attrs.get("country", "")),
        lower(attrs.get("country-code", "")),
        lower(attrs.get("tvg-name", "")),
        lower(name),
        lower(group),
        lower(url),
    ])

    # Explicit international source = foreign unless Cricket.
    if source_is_international(source_file):
        return False

    # Explicit foreign country/channel markers.
    if contains_foreign_marker(text):
        return False

    if contains_foreign_channel_marker(text):
        return False

    # Foreign ccTLDs in stream host.
    try:
        host = urlparse(url).hostname or ""
        host = host.lower()

        foreign_tlds = (
            ".uk",
            ".au",
            ".nz",
            ".za",
            ".pk",
            ".bd",
            ".lk",
            ".np",
            ".ca",
            ".sg",
            ".my",
            ".qa",
            ".ae",
        )

        if host.endswith(foreign_tlds):
            return False

    except Exception:
        pass

    return True


# ============================================================
# BUILD EXTINF
# ============================================================

def build_group(category):
    return category


def rewrite_extinf(line, attrs, name, category, language):
    new_attrs = dict(attrs)

    new_attrs["group-title"] = build_group(category)

    if language:
        new_attrs["tvg-language"] = language

    # Rebuild attributes.
    prefix = "#EXTINF:-1"

    preferred = [
        "tvg-id",
        "tvg-name",
        "tvg-logo",
        "tvg-language",
        "tvg-country",
        "group-title",
    ]

    used = set()

    parts = []

    for key in preferred:
        if key in new_attrs and new_attrs[key] != "":
            parts.append(
                f'{key}="{new_attrs[key]}"'
            )
            used.add(key)

    for key, value in new_attrs.items():
        if key in used:
            continue

        if value == "":
            continue

        parts.append(
            f'{key}="{value}"'
        )

    return prefix + " " + " ".join(parts) + "," + name


# ============================================================
# PARSE PLAYLIST
# ============================================================

def parse_m3u(path):
    entries = []

    try:
        lines = Path(path).read_text(
            encoding="utf-8",
            errors="ignore",
        ).splitlines()
    except Exception as e:
        print(f"WARNING: cannot read {path}: {e}")
        return entries

    pending_extinf = None
    pending_attrs = None
    pending_name = None

    for raw in lines:
        line = raw.strip()

        if not line:
            continue

        if line.startswith("#EXTINF:"):
            pending_extinf = line

            pending_attrs, pending_name = parse_extinf(line)

            continue

        if line.startswith("#"):
            continue

        # URL line.
        if pending_extinf:
            url = clean(line)

            if url.startswith(("http://", "https://")):
                entries.append({
                    "attrs": pending_attrs or {},
                    "name": pending_name or "",
                    "url": url,
                    "source": str(path),
                })

            pending_extinf = None
            pending_attrs = None
            pending_name = None

    return entries


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Build Indian IPTV playlist with foreign Cricket allowed."
    )

    parser.add_argument(
        "source",
        help="Source directory containing M3U files",
    )

    parser.add_argument(
        "-o",
        "--output",
        default="playlist.m3u",
        help="Output playlist",
    )

    args = parser.parse_args()

    source_dir = Path(args.source)

    if not source_dir.exists():
        raise SystemExit(
            f"ERROR: source directory not found: {source_dir}"
        )

    files = sorted(
        list(source_dir.glob("*.m3u"))
        + list(source_dir.glob("*.m3u8"))
    )

    if not files:
        raise SystemExit(
            "ERROR: no M3U/M3U8 files found."
        )

    print("========================================")
    print(" IPTV PLAYLIST GENERATOR")
    print("========================================")
    print("Sources:")

    for f in files:
        print(" -", f)

    all_entries = []

    for path in files:
        entries = parse_m3u(path)

        print(
            f"{path.name}: {len(entries)} entries"
        )

        all_entries.extend(entries)

    print(
        f"TOTAL SOURCE ENTRIES: {len(all_entries)}"
    )

    # ========================================================
    # FILTER + EXACT URL DEDUP
    # ========================================================

    final_entries = []

    seen_urls = set()

    removed_foreign = 0
    removed_excluded = 0
    removed_uncategorized = 0
    duplicate_urls = 0

    for entry in all_entries:
        attrs = entry["attrs"]
        name = entry["name"]
        url = entry["url"]
        source = entry["source"]

        group = attrs.get("group-title", "")

        # First foreign filtering.
        if not is_indian_or_allowed_cricket(
            attrs,
            name,
            group,
            url,
            source,
        ):
            removed_foreign += 1
            continue

        category = classify(
            attrs,
            name,
            url,
            source,
        )

        if not category:
            removed_uncategorized += 1
            continue

        if category not in ALLOWED_CATEGORIES:
            removed_excluded += 1
            continue

        # Exact stream URL duplicate only.
        if url in seen_urls:
            duplicate_urls += 1
            continue

        seen_urls.add(url)

        language = detect_language(
            attrs,
            name,
            group,
        )

        new_extinf = rewrite_extinf(
            entry.get("raw_extinf", ""),
            attrs,
            name,
            category,
            language,
        )

        final_entries.append({
            "extinf": new_extinf,
            "url": url,
            "category": category,
            "name": name,
            "language": language,
        })

    # ========================================================
    # SORT
    # ========================================================

    category_order = {
        "News": 1,
        "Entertainment": 2,
        "Movies": 3,
        "Music": 4,
        "Kids": 5,
        "Infotainment": 6,
        "Science": 7,
        "Lifestyle": 8,
        "Business": 9,
        "Sports": 10,
    }

    final_entries.sort(
        key=lambda x: (
            category_order.get(x["category"], 999),
            x["language"],
            x["name"].lower(),
            x["url"],
        )
    )

    # ========================================================
    # WRITE PLAYLIST
    # ========================================================

    output = Path(args.output)

    with output.open(
        "w",
        encoding="utf-8",
        newline="\n",
    ) as f:

        f.write(
            '#EXTM3U '
            'x-tvg-url="https://raw.githubusercontent.com/Sri014/3502/main/epg.xml"\n'
        )

        for entry in final_entries:
            f.write(entry["extinf"] + "\n")
            f.write(entry["url"] + "\n")

    # ========================================================
    # STATS
    # ========================================================

    counts = {}

    for entry in final_entries:
        cat = entry["category"]
        counts[cat] = counts.get(cat, 0) + 1

    print()
    print("========================================")
    print(" RESULT")
    print("========================================")

    print(
        f"FINAL CHANNELS: {len(final_entries)}"
    )

    print(
        f"FOREIGN REMOVED: {removed_foreign}"
    )

    print(
        f"UNCATEGORIZED REMOVED: {removed_uncategorized}"
    )

    print(
        f"DUPLICATE URL REMOVED: {duplicate_urls}"
    )

    print()
    print("GROUPS:")

    for category in ALLOWED_CATEGORIES:
        print(
            f"  {category}: {counts.get(category, 0)}"
        )

    print()
    print(
        f"OUTPUT: {output}"
    )


if __name__ == "__main__":
    main()
