#!/usr/bin/env python3

import os
import re
import sys
import glob
import argparse


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
    "Sports",
}


# ============================================================
# FOREIGN COUNTRY MARKERS
# ============================================================

FOREIGN_MARKERS = {
    "usa",
    "united states",
    "america",

    "uk",
    "united kingdom",
    "england",

    "canada",

    "australia",
    "new zealand",

    "pakistan",
    "pak",

    "bangladesh",
    "bd",

    "nepal",

    "sri lanka",
    "srilanka",

    "uae",
    "dubai",

    "qatar",
    "saudi",
    "saudi arabia",

    "singapore",
    "malaysia",

    "indonesia",
    "thailand",
    "philippines",

    "japan",
    "china",
    "south korea",
    "korea",

    "france",
    "germany",
    "italy",
    "spain",
    "portugal",
    "netherlands",
    "belgium",
    "ireland",

    "south africa",

    "brazil",
    "mexico",
    "argentina",
}


# ============================================================
# CHANNEL NAME -> CATEGORY
# ============================================================

CHANNEL_MAP = {

    # ========================================================
    # NEWS
    # ========================================================

    "aaj tak": "News",
    "abp news": "News",
    "india tv": "News",
    "ndtv india": "News",
    "ndtv 24x7": "News",
    "ndtv 24 x 7": "News",
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

    # ========================================================
    # BUSINESS
    # ========================================================

    "cnbc": "Business",
    "cnbc tv18": "Business",
    "cnbc tv18 prime": "Business",
    "cnbc awaaz": "Business",
    "ndtv profit": "Business",
    "ndtv profit prime": "Business",
    "bloomberg": "Business",
    "bloomberg tv": "Business",
    "business today": "Business",
    "business news": "Business",

    # ========================================================
    # MOVIES
    # ========================================================

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
    "anmol cinema 2": "Movies",

    "star utsav movies": "Movies",

    "zee biskope": "Movies",

    "epic bhojpuri": "Movies",
    "bhojpuri cinema": "Movies",

    # ========================================================
    # ENTERTAINMENT
    # ========================================================

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

    "big magic": "Entertainment",
    "dangal": "Entertainment",
    "dangal 2": "Entertainment",

    "epic bharat": "Entertainment",

    "ishara": "Entertainment",
    "utv bindass": "Entertainment",

    # ========================================================
    # MUSIC
    # ========================================================

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

    # ========================================================
    # KIDS
    # ========================================================

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

    # ========================================================
    # SCIENCE
    # ========================================================

    "discovery science": "Science",
    "science channel": "Science",
    "nasa tv": "Science",
    "nasa": "Science",
    "pbs science": "Science",

    # ========================================================
    # LIFESTYLE
    # ========================================================

    "tlc": "Lifestyle",
    "travelxp": "Lifestyle",
    "travel xp": "Lifestyle",

    "good times": "Lifestyle",
    "food food": "Lifestyle",

    "fashion tv": "Lifestyle",
    "fashiontv": "Lifestyle",
    "fmc": "Lifestyle",

    # ========================================================
    # INFOTAINMENT
    # ========================================================

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
    "epic": "Infotainment",
    "epic channel": "Infotainment",

    "investigation discovery": "Infotainment",

    # ========================================================
    # CRICKET / SPORTS
    # ========================================================

    "star sports 1": "Sports",
    "star sports 1 hd": "Sports",
    "star sports 1 hindi": "Sports",
    "star sports 1 hindi hd": "Sports",

    "star sports 2": "Sports",
    "star sports 2 hd": "Sports",

    "star sports 3": "Sports",
    "star sports 3 hd": "Sports",

    "star sports first": "Sports",
    "star sports khel": "Sports",
    "star sports khel hd": "Sports",

    "star sports tamil": "Sports",
    "star sports telugu": "Sports",
    "star sports kannada": "Sports",
    "star sports bangla": "Sports",

    "sony sports ten 1": "Sports",
    "sony ten 1": "Sports",

    "sony sports ten 2": "Sports",
    "sony ten 2": "Sports",

    "sony sports ten 3": "Sports",
    "sony ten 3": "Sports",

    "sony sports ten 4": "Sports",
    "sony ten 4": "Sports",

    "sony sports ten 5": "Sports",
    "sony ten 5": "Sports",

    "willow": "Sports",
    "willow cricket": "Sports",

    "dd sports": "Sports",

    "football": "Sports",
    "football hd": "Sports",
    "soccer": "Sports",

    "bein sports": "Sports",
    "beinsports": "Sports",

    "euro sport": "Sports",
    "eurosport": "Sports",

    "hockey": "Sports",
    "hockey india": "Sports",
    "star sports hockey": "Sports",

    "tennis": "Sports",
    "tennis channel": "Sports",

    # ========================================================
    # INDIAN LANGUAGE CHANNELS
    # ========================================================

    # Bengali
    "zee 24 ghanta": "News",
    "abp ananda": "News",

    # Tamil
    "sun tv": "Entertainment",
    "sun news": "News",
    "sun music": "Music",
    "kalaignar": "Entertainment",

    # Telugu
    "etv telugu": "Entertainment",
    "sakshi tv": "News",

    # Kannada
    "udaya": "Entertainment",
    "suvarna": "Entertainment",
    "public tv": "News",

    # Malayalam
    "asianet": "Entertainment",
    "surya tv": "Entertainment",
    "mazhavil": "Entertainment",

    # Marathi
    "zee 24 taas": "News",
    "abp majha": "News",

    # Punjabi
    "zee punjabi": "Entertainment",
    "ptc": "Entertainment",
    "chardikla": "Entertainment",

    # Gujarati
    "abp asmita": "News",
    "sandesh": "News",

    # Odia
    "otv": "News",
    "kanak news": "News",
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

    "Assamese": [
        "assamese",
        "assam",
        "pratidin",
    ],
}


# ============================================================
# HELPERS
# ============================================================

def clean(value):
    if not value:
        return ""

    value = value.lower().strip()

    value = re.sub(
        r"\[[^\]]*\]",
        " ",
        value
    )

    value = re.sub(
        r"\([^)]*\)",
        " ",
        value
    )

    value = re.sub(
        r"\{[^}]*\}",
        " ",
        value
    )

    value = value.replace("_", " ")
    value = value.replace("-", " ")

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


def parse_extinf(line):
    attrs = {}

    if "," in line:
        info = line.split(",", 1)[1].strip()
    else:
        info = ""

    for key, value in re.findall(
        r'([\w-]+)="([^"]*)"',
        line
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


# ============================================================
# FOREIGN STREAM DETECTION
# ============================================================

def is_foreign_stream(
    attrs,
    name="",
    group="",
    url=""
):
    """
    Removes streams which are explicitly identified
    as belonging to another country.

    IMPORTANT:
    Unknown streams are NOT removed.

    This means Indian streams without country metadata
    are retained.
    """

    # --------------------------------------------------------
    # Country metadata
    # --------------------------------------------------------

    country_fields = [
        attrs.get("tvg-country", ""),
        attrs.get("country", ""),
        attrs.get("region", ""),
        attrs.get("geo", ""),
        attrs.get("country-code", ""),
        attrs.get("country_code", ""),
    ]

    country_text = clean(
        " ".join(country_fields)
    )

    if country_text:

        # Explicit India
        if (
            country_text == "india"
            or country_text == "in"
            or "india" in country_text
        ):
            return False

        # Explicit foreign country
        for marker in FOREIGN_MARKERS:

            marker_clean = clean(marker)

            if marker_clean in {
                "us",
                "uk",
                "in",
                "bd",
                "pak",
            }:
                continue

            if marker_clean in country_text:
                return True

    # --------------------------------------------------------
    # Name + group
    # --------------------------------------------------------

    text = clean(
        " ".join([
            name,
            group,
        ])
    )

    # Explicit foreign country names.
    # Avoid tiny ambiguous words such as "us".
    for marker in FOREIGN_MARKERS:

        marker_clean = clean(marker)

        if marker_clean in {
            "us",
            "uk",
            "in",
            "bd",
            "pak",
        }:
            continue

        if marker_clean in text:
            return True

    # --------------------------------------------------------
    # URL/domain hints
    # --------------------------------------------------------

    u = url.lower()

    foreign_domains = [
        ".pk/",
        ".pk:",
        ".bd/",
        ".bd:",
        ".lk/",
        ".lk:",
        ".np/",
        ".np:",
        ".uk/",
        ".uk:",
        ".ca/",
        ".ca:",
        ".au/",
        ".au:",
        ".nz/",
        ".nz:",
        ".za/",
        ".za:",
        ".sg/",
        ".sg:",
        ".my/",
        ".my:",
    ]

    if any(
        x in u
        for x in foreign_domains
    ):
        return True

    return False


# ============================================================
# CHANNEL MAPPING
# ============================================================

def find_exact_mapping(name):

    n = clean(name)

    if not n:
        return None

    # Exact
    if n in CHANNEL_MAP:
        return CHANNEL_MAP[n]

    # Longest match first
    matches = []

    for key, category in CHANNEL_MAP.items():

        k = clean(key)

        if k and k in n:
            matches.append(
                (
                    len(k),
                    category
                )
            )

    if matches:
        matches.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return matches[0][1]

    return None


# ============================================================
# SPORTS
# ============================================================

def detect_sport(
    name,
    group=""
):

    text = clean(
        name + " " + group
    )

    cricket_words = [
        "cricket",
        "star sports",
        "sony sports",
        "sony ten",
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

    if any(
        x in text
        for x in cricket_words
    ):
        return "Sports"

    if any(
        x in text
        for x in football_words
    ):
        return "Sports"

    if any(
        x in text
        for x in hockey_words
    ):
        return "Sports"

    if any(
        x in text
        for x in tennis_words
    ):
        return "Sports"

    return None


# ============================================================
# LANGUAGE
# ============================================================

def detect_language(
    name,
    group="",
    attrs=None
):

    attrs = attrs or {}

    text = clean(
        " ".join([
            name,
            group,
            attrs.get(
                "tvg-language",
                ""
            ),
            attrs.get(
                "language",
                ""
            ),
        ])
    )

    for language, words in LANGUAGE_WORDS.items():

        for word in words:

            if clean(word) in text:
                return language

    return "Unknown"


# ============================================================
# OLD GROUP -> NEW GROUP
# ============================================================

def category_from_old_group(group):

    g = clean(group)

    if not g:
        return None

    # Explicit exclusions
    if any(
        x in g
        for x in EXCLUDED_GROUPS
    ):
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

        "lifestyle": "Lifestyle",

        "business": "Business",

        "sports": "Sports",
        "sport": "Sports",
    }

    for key, category in aliases.items():

        if key in g:
            return category

    return None


# ============================================================
# KEYWORD CATEGORY
# ============================================================

def keyword_category(
    name,
    old_group
):

    text = clean(
        name + " " + old_group
    )

    # --------------------------------------------------------
    # Exclusions
    # --------------------------------------------------------

    excluded_words = [
        "devotional",
        "bhakti",
        "spiritual",
        "education",
        "educational",
        "learning",
        "regional",
    ]

    if any(
        x in text
        for x in excluded_words
    ):
        return None

    # --------------------------------------------------------
    # Sports first
    # --------------------------------------------------------

    sport = detect_sport(
        name,
        old_group
    )

    if sport:
        return sport

    # --------------------------------------------------------
    # News
    # --------------------------------------------------------

    if any(
        x in text
        for x in [
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
        ]
    ):
        return "News"

    # --------------------------------------------------------
    # Business
    # --------------------------------------------------------

    if any(
        x in text
        for x in [
            "business",
            "cnbc",
            "bloomberg",
            "profit",
            "market",
            "money",
        ]
    ):
        return "Business"

    # --------------------------------------------------------
    # Kids
    # --------------------------------------------------------

    if any(
        x in text
        for x in [
            "kids",
            "cartoon",
            "nick",
            "disney junior",
            "pogo",
            "hungama",
            "sonic",
            "cbeebies",
        ]
    ):
        return "Kids"

    # --------------------------------------------------------
    # Music
    # --------------------------------------------------------

    if any(
        x in text
        for x in [
            "music",
            "mtv",
            "9xm",
            "b4u music",
            "vh1",
            "mastiii",
            "zoom",
        ]
    ):
        return "Music"

    # --------------------------------------------------------
    # Movies
    # --------------------------------------------------------

    if any(
        x in text
        for x in [
            "movie",
            "movies",
            "cinema",
            "pictures",
            "film",
            "filmy",
            "max",
            "gold",
            "cineplex",
        ]
    ):
        return "Movies"

    # --------------------------------------------------------
    # Science
    # --------------------------------------------------------

    if any(
        x in text
        for x in [
            "science",
            "nasa",
        ]
    ):
        return "Science"

    # --------------------------------------------------------
    # Lifestyle
    # --------------------------------------------------------

    if any(
        x in text
        for x in [
            "lifestyle",
            "travel",
            "food",
            "fashion",
            "tlc",
        ]
    ):
        return "Lifestyle"

    # --------------------------------------------------------
    # Infotainment
    # --------------------------------------------------------

    if any(
        x in text
        for x in [
            "discovery",
            "animal planet",
            "history",
            "nat geo",
            "national geographic",
            "earth",
            "documentary",
            "wild",
        ]
    ):
        return "Infotainment"

    # --------------------------------------------------------
    # Existing source group
    # --------------------------------------------------------

    return category_from_old_group(
        old_group
    )


# ============================================================
# CLASSIFICATION
# ============================================================

def classify(
    attrs,
    url=""
):

    name = get_channel_name(
        attrs
    )

    old_group = (
        attrs.get("group-title")
        or attrs.get("group")
        or ""
    )

    # --------------------------------------------------------
    # Foreign filter
    # --------------------------------------------------------

    if is_foreign_stream(
        attrs,
        name,
        old_group,
        url
    ):
        return None, None

    # --------------------------------------------------------
    # Channel mapping
    # --------------------------------------------------------

    category = find_exact_mapping(
        name
    )

    # --------------------------------------------------------
    # Sports
    # --------------------------------------------------------

    sport = detect_sport(
        name,
        old_group
    )

    if sport:
        category = sport

    # --------------------------------------------------------
    # Keyword/source group
    # --------------------------------------------------------

    if not category:

        category = keyword_category(
            name,
            old_group
        )

    # --------------------------------------------------------
    # Excluded
    # --------------------------------------------------------

    if category:

        if clean(category) in EXCLUDED_GROUPS:
            category = None

    # --------------------------------------------------------
    # Safe fallback
    # --------------------------------------------------------

    if not category:
        category = "Entertainment"

    # --------------------------------------------------------
    # Normalize sports
    # --------------------------------------------------------

    if category == "Sports":
        category = "Sports"

    # --------------------------------------------------------
    # Safety: only allowed groups
    # --------------------------------------------------------

    if category not in ALLOWED_CATEGORIES:
        category = "Entertainment"

    language = detect_language(
        name,
        old_group,
        attrs
    )

    return language, category


# ============================================================
# GROUP NAME
# ============================================================

def build_group(
    language,
    category
):

    # Language is metadata only.
    #
    # NEVER:
    # Hindi - News
    # Tata Play - News
    # JioTV - News
    #
    # ONLY:
    # News
    # Sports
    # Movies
    # etc.

    return category


# ============================================================
# PARSE M3U
# ============================================================

def parse_m3u(path):

    entries = []

    try:

        with open(
            path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            lines = [
                x.rstrip("\n")
                for x in f
            ]

    except Exception as e:

        print(
            "ERROR reading:",
            path,
            e
        )

        return entries

    current = None

    for line in lines:

        if line.startswith(
            "#EXTINF:"
        ):

            current = {
                "extinf": line,
                "attrs": parse_extinf(
                    line
                ),
                "url": "",
            }

        elif (
            current
            and line.strip()
            and not line.startswith("#")
        ):

            current["url"] = (
                line.strip()
            )

            entries.append(
                current
            )

            current = None

    return entries


# ============================================================
# REWRITE EXTINF
# ============================================================

def rewrite_extinf(entry):

    line = entry["extinf"]

    attrs = entry["attrs"]

    url = entry["url"]

    language, category = classify(
        attrs,
        url
    )

    # Foreign/rejected stream
    if not category:
        return None

    group = build_group(
        language,
        category
    )

    # --------------------------------------------------------
    # Remove old group-title
    # --------------------------------------------------------

    line = re.sub(
        r'\s*group-title="[^"]*"',
        "",
        line,
        flags=re.I
    )

    # --------------------------------------------------------
    # Remove old tvg-language
    # --------------------------------------------------------

    line = re.sub(
        r'\s*tvg-language="[^"]*"',
        "",
        line,
        flags=re.I
    )

    # --------------------------------------------------------
    # Add group
    # --------------------------------------------------------

    line = (
        line.rstrip()
        + f' group-title="{group}"'
    )

    # --------------------------------------------------------
    # Add language
    # --------------------------------------------------------

    if language != "Unknown":

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
        description=(
            "Build grouped Indian IPTV playlist"
        )
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

    source = os.path.abspath(
        args.source
    )

    if not os.path.isdir(source):

        print(
            "ERROR: source directory not found:",
            source
        )

        sys.exit(1)

    # --------------------------------------------------------
    # Find M3U/M3U8
    # --------------------------------------------------------

    files = []

    files.extend(
        glob.glob(
            os.path.join(
                source,
                "**",
                "*.m3u"
            ),
            recursive=True
        )
    )

    files.extend(
        glob.glob(
            os.path.join(
                source,
                "**",
                "*.m3u8"
            ),
            recursive=True
        )
    )

    files = sorted(
        set(files)
    )

    if not files:

        print(
            "ERROR: No M3U/M3U8 files found"
        )

        sys.exit(1)

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    print()
    print(
        "=========================================="
    )
    print(
        " IPTV GROUP BUILDER"
    )
    print(
        "=========================================="
    )

    print(
        "Source:",
        source
    )

    print(
        "M3U files:",
        len(files)
    )

    print()

    # --------------------------------------------------------
    # Read all entries
    # --------------------------------------------------------

    all_entries = []

    for path in files:

        print(
            "Reading:",
            path
        )

        entries = parse_m3u(
            path
        )

        all_entries.extend(
            entries
        )

        print(
            "  channels:",
            len(entries)
        )

    print()

    print(
        "Total source streams:",
        len(all_entries)
    )

    # --------------------------------------------------------
    # Output
    # --------------------------------------------------------

    output = os.path.abspath(
        args.output
    )

    seen_urls = set()

    written = 0

    skipped_foreign = 0

    skipped_duplicate = 0

    skipped_empty = 0

    group_counts = {}

    language_counts = {}

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

            url = (
                entry["url"]
                .strip()
            )

            # ------------------------------------------------
            # Empty URL
            # ------------------------------------------------

            if not url:

                skipped_empty += 1

                continue

            # ------------------------------------------------
            # Exact URL duplicate
            # ------------------------------------------------

            if url in seen_urls:

                skipped_duplicate += 1

                continue

            # ------------------------------------------------
            # Classify
            # ------------------------------------------------

            extinf = rewrite_extinf(
                entry
            )

            # ------------------------------------------------
            # Foreign/rejected
            # ------------------------------------------------

            if not extinf:

                skipped_foreign += 1

                continue

            # ------------------------------------------------
            # Mark URL as used
            # ------------------------------------------------

            seen_urls.add(
                url
            )

            # ------------------------------------------------
            # Write
            # ------------------------------------------------

            f.write(
                extinf + "\n"
            )

            f.write(
                url + "\n"
            )

            written += 1

            # ------------------------------------------------
            # Statistics
            # ------------------------------------------------

            attrs = entry["attrs"]

            name = get_channel_name(
                attrs
            )

            old_group = (
                attrs.get(
                    "group-title",
                    ""
                )
            )

            language, category = classify(
                attrs,
                url
            )

            if category:

                group_counts[
                    category
                ] = (
                    group_counts.get(
                        category,
                        0
                    ) + 1
                )

            if language:

                language_counts[
                    language
                ] = (
                    language_counts.get(
                        language,
                        0
                    ) + 1
                )

    # ========================================================
    # FINAL REPORT
    # ========================================================

    print()

    print(
        "=========================================="
    )

    print(
        " DONE"
    )

    print(
        "=========================================="
    )

    print(
        "Output:",
        output
    )

    print(
        "Written streams:",
        written
    )

    print(
        "Foreign/rejected:",
        skipped_foreign
    )

    print(
        "Exact duplicate URLs:",
        skipped_duplicate
    )

    print(
        "Empty URLs:",
        skipped_empty
    )

    print()

    # --------------------------------------------------------
    # Groups
    # --------------------------------------------------------

    print(
        "GROUP COUNTS:"
    )

    group_order = [
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
    ]

    for group in group_order:

        print(
            f"  {group}: "
            f"{group_counts.get(group, 0)}"
        )

    print()

    # --------------------------------------------------------
    # Languages
    # --------------------------------------------------------

    print(
        "LANGUAGES:"
    )

    for language in sorted(
        language_counts
    ):

        print(
            f"  {language}: "
            f"{language_counts[language]}"
        )

    print()

    print(
        "Excluded:"
    )

    print(
        "  Regional"
    )

    print(
        "  Devotional"
    )

    print(
        "  Education"
    )

    print(
        "  Spiritual"
    )

    print()

    print(
        "Duplicate policy:"
    )

    print(
        "  Same URL      = REMOVE"
    )

    print(
        "  Different URL = KEEP"
    )

    print()

    print(
        "Sports:"
    )

    print(
        "  All sports -> Sports"
    )

    print(
        "=========================================="
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
