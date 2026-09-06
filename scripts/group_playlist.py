#!/usr/bin/env python3

import os
import re
import sys
import glob
import argparse
from urllib.parse import urlparse

# ============================================================
# CONFIG
# ============================================================

EXCLUDED_GROUPS = {
    "regional",
    "devotional",
    "education",
    "spiritual",
}

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
}

SPORTS_CATEGORIES = {
    "Cricket",
    "Football",
    "Hockey",
    "Tennis",
    "Sports",
}

# ============================================================
# CHANNEL NAME -> CATEGORY
# Tata Play / JioTV-style classification
# ============================================================

CHANNEL_MAP = {

    # ---------------- NEWS ----------------

    "aaj tak": "News",
    "abp news": "News",
    "india tv": "News",
    "ndtv india": "News",
    "ndtv 24x7": "News",
    "news18 india": "News",
    "news18": "News",
    "zee news": "News",
    "times now": "News",
    "times now navbharat": "News",
    "republic tv": "News",
    "republic bharat": "News",
    "india today": "News",
    "cnn": "News",
    "cnn international": "News",
    "bbc news": "News",
    "bbc world news": "News",
    "bbc world": "News",
    "al jazeera": "News",
    "wion": "News",
    "mirror now": "News",
    "et now": "News",
    "et now swadesh": "News",
    "cnbc tv18": "Business",
    "cnbc tv18 prime": "Business",
    "cnbc awaaz": "Business",
    "ndtv profit": "Business",
    "ndtv profit prime": "Business",
    "bloomberg": "Business",
    "business today": "Business",

    # ---------------- MOVIES ----------------

    "zee cinema": "Movies",
    "zee cinema hd": "Movies",
    "star gold": "Movies",
    "star gold hd": "Movies",
    "star gold 2": "Movies",
    "star gold select": "Movies",
    "star gold romance": "Movies",
    "star gold thrills": "Movies",
    "star movies": "Movies",
    "star movies hd": "Movies",
    "star movies select": "Movies",
    "movies now": "Movies",
    "movies now hd": "Movies",
    "mnx": "Movies",
    "mn+": "Movies",
    "romedy now": "Movies",
    "&pictures": "Movies",
    "colors cineplex": "Movies",
    "sony max": "Movies",
    "sony max 2": "Movies",
    "sony wah": "Movies",
    "b4u movies": "Movies",
    "b4u kadak": "Movies",
    "goldmines": "Movies",
    "goldmines movies": "Movies",
    "action cinema": "Movies",
    "anmol cinema": "Movies",
    "star utsav movies": "Movies",
    "zee biskope": "Movies",
    "epic bhojpuri": "Movies",
    "bhojpuri cinema": "Movies",

    # ---------------- ENTERTAINMENT ----------------

    "zee tv": "Entertainment",
    "star plus": "Entertainment",
    "star bharat": "Entertainment",
    "colors": "Entertainment",
    "colors hd": "Entertainment",
    "&tv": "Entertainment",
    "sony entertainment television": "Entertainment",
    "sony sab": "Entertainment",
    "sab tv": "Entertainment",
    "sony pal": "Entertainment",
    "star utsav": "Entertainment",
    "anmol tv": "Entertainment",
    "anmol cinema 2": "Entertainment",
    "big magic": "Entertainment",
    "dangal": "Entertainment",
    "dangal 2": "Entertainment",
    "epic": "Infotainment",
    "epic bharat": "Entertainment",
    "ishara": "Entertainment",
    "utv bindass": "Entertainment",
    "investigation discovery": "Infotainment",

    # ---------------- MUSIC ----------------

    "mtv": "Music",
    "mtv hd": "Music",
    "9xm": "Music",
    "9x music": "Music",
    "9x jhakaas": "Music",
    "b4u music": "Music",
    "zoom": "Music",
    "mastiii": "Music",
    "music india": "Music",
    "music zone": "Music",
    "vh1": "Music",
    "vh1 hd": "Music",
    "zing": "Music",
    "dhamaka music": "Music",
    "epic music": "Music",
    "sun music": "Music",
    "sun music hd": "Music",
    "sun gemini music": "Music",
    "sun surya music": "Music",
    "sun udaya music": "Music",
    "star maa music": "Music",
    "star maa music hd": "Music",

    # ---------------- KIDS ----------------

    "cartoon network": "Kids",
    "pogo": "Kids",
    "nick": "Kids",
    "nick jr": "Kids",
    "nickelodeon": "Kids",
    "sonic": "Kids",
    "disney": "Kids",
    "disney junior": "Kids",
    "disney channel": "Kids",
    "hungama": "Kids",
    "super hungama": "Kids",
    "discovery kids": "Kids",
    "epic kids": "Kids",
    "etv bal bharat": "Kids",
    "cbeebies": "Kids",
    "unique tv": "Kids",
    "kushi tv": "Kids",

    # ---------------- SCIENCE ----------------

    "discovery science": "Science",
    "science channel": "Science",
    "nasa tv": "Science",
    "nasa": "Science",
    "pbs science": "Science",

    # ---------------- LIFESTYLE ----------------

    "tlc": "Lifestyle",
    "travelxp": "Lifestyle",
    "travel xp": "Lifestyle",
    "good times": "Lifestyle",
    "food food": "Lifestyle",
    "fashion tv": "Lifestyle",
    "fmc": "Lifestyle",
    "fashiontv": "Lifestyle",

    # ---------------- INFOTAINMENT ----------------

    "discovery channel": "Infotainment",
    "animal planet": "Infotainment",
    "history tv": "Infotainment",
    "history": "Infotainment",
    "discovery turbo": "Infotainment",
    "discovery civilization": "Infotainment",
    "nat geo": "Infotainment",
    "national geographic": "Infotainment",
    "natgeo": "Infotainment",
    "sony bbc earth": "Infotainment",
    "bbc earth": "Infotainment",
    "wild": "Infotainment",
    "epic channel": "Infotainment",

    # ---------------- BUSINESS ----------------

    "cnbc": "Business",
    "cnbc tv18": "Business",
    "cnbc tv18 prime": "Business",
    "cnbc awaaz": "Business",
    "ndtv profit": "Business",
    "ndtv profit prime": "Business",
    "bloomberg tv": "Business",
    "business news": "Business",

    # ---------------- CRICKET ----------------

    "star sports 1": "Cricket",
    "star sports 1 hd": "Cricket",
    "star sports 1 hindi": "Cricket",
    "star sports 1 hindi hd": "Cricket",
    "star sports 2": "Cricket",
    "star sports 2 hd": "Cricket",
    "star sports 3": "Cricket",
    "star sports 3 hd": "Cricket",
    "star sports first": "Cricket",
    "star sports khel": "Cricket",
    "star sports khel hd": "Cricket",
    "star sports tamil": "Cricket",
    "star sports telugu": "Cricket",
    "star sports kannada": "Cricket",
    "star sports bangla": "Cricket",
    "sony sports ten 1": "Cricket",
    "sony ten 1": "Cricket",
    "sony sports ten 2": "Cricket",
    "sony ten 2": "Cricket",
    "sony sports ten 3": "Cricket",
    "sony ten 3": "Cricket",
    "willow": "Cricket",
    "willow cricket": "Cricket",
    "dd sports": "Cricket",

    # ---------------- FOOTBALL ----------------

    "sony sports ten 2": "Football",
    "sony sports ten 5": "Football",
    "sony ten 5": "Football",
    "football": "Football",
    "football hd": "Football",
    "bein sports": "Football",
    "beinsports": "Football",
    "euro sport": "Football",
    "eurosport": "Football",

    # ---------------- HOCKEY ----------------

    "hockey": "Hockey",
    "hockey india": "Hockey",
    "star sports hockey": "Hockey",

    # ---------------- TENNIS ----------------

    "tennis": "Tennis",
    "tennis channel": "Tennis",
    "sony sports ten 4": "Tennis",
    "sony ten 4": "Tennis",
}


# ============================================================
# LANGUAGE DETECTION
# ============================================================

LANGUAGE_WORDS = {
    "Hindi": [
        "hindi",
        "hind",
        "bharat",
        "navbharat",
    ],

    "English": [
        "english",
        "bbc",
        "cnn",
        "bloomberg",
        "discovery",
        "national geographic",
        "animal planet",
        "tlc",
        "travelxp",
        "eurosport",
    ],

    "Bhojpuri": [
        "bhojpuri",
        "bhojpuriya",
        "epic bhojpuri",
        "zee biskope",
    ],

    "Bengali": [
        "bangla",
        "bengali",
        "zee 24 ghanta",
        "abp ananda",
    ],

    "Tamil": [
        "tamil",
        "sun tv",
        "sun music",
        "sun news",
        "kalaignar",
    ],

    "Telugu": [
        "telugu",
        "gemini",
        "etv telugu",
        "sakshi tv",
    ],

    "Kannada": [
        "kannada",
        "udaya",
        "suvarna",
        "public tv",
    ],

    "Malayalam": [
        "malayalam",
        "asianet",
        "surya tv",
        "mazhavil",
    ],

    "Marathi": [
        "marathi",
        "zee 24 taas",
        "abp majha",
    ],

    "Punjabi": [
        "punjabi",
        "zee punjabi",
        "ptc",
        "chardikla",
    ],

    "Gujarati": [
        "gujarati",
        "abp asmita",
        "sandesh",
    ],

    "Odia": [
        "odia",
        "oriya",
        "otv",
        "kanak news",
    ],
}


# ============================================================
# HELPERS
# ============================================================

def clean(value):
    if not value:
        return ""

    value = value.lower().strip()

    value = re.sub(r"\[[^\]]*\]", " ", value)
    value = re.sub(r"\([^)]*\)", " ", value)
    value = re.sub(r"\{[^}]*\}", " ", value)

    value = value.replace("_", " ")
    value = value.replace("-", " ")

    value = re.sub(r"\s+", " ", value)

    return value.strip()


def parse_extinf(line):
    attrs = {}

    if "," in line:
        info = line.split(",", 1)[1].strip()
    else:
        info = ""

    for key, value in re.findall(
        r'([\w-]+)="([^"]*)"', line
    ):
        attrs[key.lower()] = value

    attrs["_name"] = info

    return attrs


def get_channel_name(attrs):
    return (
        attrs.get("tvg-name")
        or attrs.get("_name")
        or attrs.get("name")
        or ""
    ).strip()


def find_exact_mapping(name):
    n = clean(name)

    if not n:
        return None

    # exact first
    if n in CHANNEL_MAP:
        return CHANNEL_MAP[n]

    # longest known channel name first
    matches = []

    for key, category in CHANNEL_MAP.items():
        k = clean(key)

        if k and k in n:
            matches.append((len(k), category))

    if matches:
        matches.sort(reverse=True)
        return matches[0][1]

    return None


def detect_sport(name, group=""):
    text = clean(name + " " + group)

    # IMPORTANT:
    # Check specific sports before generic sports.

    cricket_words = [
        "cricket",
        "star sports",
        "sony ten 1",
        "sony ten 2",
        "sony ten 3",
        "willow",
        "dd sports",
    ]

    football_words = [
        "football",
        "soccer",
        "premier league",
        "uefa",
        "champions league",
        "la liga",
        "bundesliga",
        "fifa",
        "bein sports",
    ]

    hockey_words = [
        "hockey",
        "hockey india",
    ]

    tennis_words = [
        "tennis",
        "atp",
        "wta",
        "roland garros",
        "wimbledon",
        "us open tennis",
        "australian open tennis",
    ]

    if any(x in text for x in cricket_words):
        return "Cricket"

    if any(x in text for x in football_words):
        return "Football"

    if any(x in text for x in hockey_words):
        return "Hockey"

    if any(x in text for x in tennis_words):
        return "Tennis"

    return None


def detect_language(name, group="", attrs=None):
    attrs = attrs or {}

    text = clean(
        " ".join([
            name,
            group,
            attrs.get("tvg-language", ""),
            attrs.get("language", ""),
        ])
    )

    for language, words in LANGUAGE_WORDS.items():
        for word in words:
            if clean(word) in text:
                return language

    return "Unknown"


def category_from_old_group(group):
    g = clean(group)

    if not g:
        return None

    # Explicit exclusions
    if any(x in g for x in EXCLUDED_GROUPS):
        return None

    aliases = {
        "news": "News",
        "entertainment": "Entertainment",
        "movies": "Movies",
        "movie": "Movies",
        "music": "Music",
        "kids": "Kids",
        "children": "Kids",
        "infotainment": "Infotainment",
        "knowledge": "Infotainment",
        "knowledge lifestyle": "Infotainment",
        "lifestyle": "Lifestyle",
        "business": "Business",
        "sports": "Sports",
    }

    for key, category in aliases.items():
        if key in g:
            return category

    return None


def keyword_category(name, old_group):
    text = clean(name + " " + old_group)

    # Never allow excluded categories
    if any(x in text for x in [
        "devotional",
        "bhakti",
        "spiritual",
        "education",
        "educational",
        "learning",
        "regional",
    ]):
        return None

    # Sports first
    sport = detect_sport(name, old_group)

    if sport:
        return sport

    # News
    if any(x in text for x in [
        "news",
        "breaking news",
        "times now",
        "republic",
        "ndtv",
        "abp news",
        "aaj tak",
        "zee news",
        "cnn",
        "bbc news",
        "al jazeera",
    ]):
        return "News"

    # Business
    if any(x in text for x in [
        "business",
        "cnbc",
        "bloomberg",
        "profit",
        "market",
        "money",
    ]):
        return "Business"

    # Kids
    if any(x in text for x in [
        "kids",
        "cartoon",
        "nick",
        "disney junior",
        "pogo",
        "hungama",
        "sonic",
        "cbeebies",
    ]):
        return "Kids"

    # Music
    if any(x in text for x in [
        "music",
        "mtv",
        "9xm",
        "b4u music",
        "vh1",
        "mastiii",
        "zoom",
    ]):
        return "Music"

    # Movies
    if any(x in text for x in [
        "movie",
        "movies",
        "cinema",
        "pictures",
        "film",
        "filmy",
        "max",
        "gold",
        "cineplex",
    ]):
        return "Movies"

    # Science
    if any(x in text for x in [
        "science",
        "nasa",
    ]):
        return "Science"

    # Lifestyle
    if any(x in text for x in [
        "lifestyle",
        "travel",
        "food",
        "fashion",
        "tlc",
    ]):
        return "Lifestyle"

    # Infotainment
    if any(x in text for x in [
        "discovery",
        "animal planet",
        "history",
        "nat geo",
        "national geographic",
        "earth",
        "documentary",
        "wild",
    ]):
        return "Infotainment"

    # Existing source group as final signal
    return category_from_old_group(old_group)


def classify(attrs):
    name = get_channel_name(attrs)

    old_group = (
        attrs.get("group-title")
        or attrs.get("group")
        or ""
    )

    # --------------------------------------------------------
    # 1. Exact channel mapping
    # --------------------------------------------------------

    category = find_exact_mapping(name)

    # --------------------------------------------------------
    # 2. Sports classification
    # --------------------------------------------------------

    sport = detect_sport(name, old_group)

    if sport:
        category = sport

    # --------------------------------------------------------
    # 3. Keyword / source-group classification
    # --------------------------------------------------------

    if not category:
        category = keyword_category(name, old_group)

    # --------------------------------------------------------
    # 4. Exclusions
    # --------------------------------------------------------

    if category:
        if clean(category) in EXCLUDED_GROUPS:
            category = None

    # --------------------------------------------------------
    # 5. Safe fallback
    # --------------------------------------------------------

    # Do not create Regional / Devotional / Education groups.
    # Unknown channels go into Entertainment rather than being lost.
    if not category:
        category = "Entertainment"

    # Normalize generic Sports
    if category == "Sports":
        category = detect_sport(name, old_group) or "Sports"

    language = detect_language(
        name,
        old_group,
        attrs
    )

    return language, category


def build_group(language, category):
    # Language is metadata, NOT part of group name.
    #
    # User specifically does not want:
    # "Tata Play - News"
    # "JioTV - News"
    # "Hindi - News"
    #
    # So final groups are simply:
    # News
    # Entertainment
    # Movies
    # etc.

    return category


def parse_m3u(path):
    entries = []

    with open(
        path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as f:
        lines = [x.rstrip("\n") for x in f]

    current = None

    for line in lines:

        if line.startswith("#EXTINF:"):
            current = {
                "extinf": line,
                "attrs": parse_extinf(line),
                "url": "",
            }

        elif current and line.strip() and not line.startswith("#"):
            current["url"] = line.strip()
            entries.append(current)
            current = None

    return entries


def rewrite_extinf(entry):
    line = entry["extinf"]
    attrs = entry["attrs"]

    language, category = classify(attrs)

    group = build_group(
        language,
        category
    )

    # Remove old group-title
    line = re.sub(
        r'\s*group-title="[^"]*"',
        "",
        line,
        flags=re.I
    )

    # Add new group
    line = (
        line.rstrip()
        + f' group-title="{group}"'
    )

    # Preserve/add language metadata
    if language != "Unknown":
        line = re.sub(
            r'\s*tvg-language="[^"]*"',
            "",
            line,
            flags=re.I
        )

        line = (
            line.rstrip()
            + f' tvg-language="{language}"'
        )

    return line


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description="Build grouped IPTV playlist"
    )

    parser.add_argument(
        "source",
        help="Directory containing M3U files"
    )

    parser.add_argument(
        "-o",
        "--output",
        default="playlist.m3u",
        help="Output playlist"
    )

    args = parser.parse_args()

    source = os.path.abspath(args.source)

    if not os.path.isdir(source):
        print("ERROR: source directory not found:", source)
        sys.exit(1)

    files = sorted(
        glob.glob(
            os.path.join(source, "**", "*.m3u"),
            recursive=True
        )
    )

    if not files:
        print("ERROR: No M3U files found")
        sys.exit(1)

    all_entries = []

    print()
    print("==========================================")
    print(" IPTV GROUP BUILDER")
    print("==========================================")
    print("Source:", source)
    print("M3U files:", len(files))
    print()

    for path in files:

        print("Reading:", path)

        try:
            entries = parse_m3u(path)
            all_entries.extend(entries)

            print(
                "  channels:",
                len(entries)
            )

        except Exception as e:
            print(
                "  ERROR:",
                e
            )

    print()
    print("Total source streams:", len(all_entries))

    # --------------------------------------------------------
    # IMPORTANT:
    # NO URL DEDUPLICATION
    #
    # Same channel from different URLs remains.
    # Same channel from different countries remains.
    # Different stream variants remain.
    # --------------------------------------------------------

    output = os.path.abspath(args.output)

    with open(
        output,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            '#EXTM3U '
            'x-tvg-url="guide.xml.gz"\n'
        )

        for entry in all_entries:

            url = entry["url"]

            if not url:
                continue

            extinf = rewrite_extinf(entry)

            f.write(extinf + "\n")
            f.write(url + "\n")

    print()
    print("==========================================")
    print(" DONE")
    print("==========================================")
    print("Output:", output)
    print("Streams:", len(all_entries))
    print()
    print("Groups:")
    print("  News")
    print("  Entertainment")
    print("  Movies")
    print("  Music")
    print("  Kids")
    print("  Infotainment")
    print("  Science")
    print("  Lifestyle")
    print("  Business")
    print("  Cricket")
    print("  Football")
    print("  Hockey")
    print("  Tennis")
    print()
    print("Excluded:")
    print("  Regional")
    print("  Devotional")
    print("  Education")
    print()
    print("Duplicates: KEPT")
    print("==========================================")


if __name__ == "__main__":
    main()
