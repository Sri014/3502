#!/usr/bin/env python3

import os
import re
import sys
import glob
import argparse


# ============================================================
# FINAL IPTV GROUP CONFIG
# ============================================================

# These groups MUST NEVER appear in final playlist
EXCLUDED_GROUPS = {
    "regional",
    "devotional",
    "education",
    "spiritual",
}


# Final allowed groups
ALLOWED_GROUPS = {
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
# CHANNEL NAME CLASSIFICATION
# ============================================================

CHANNEL_MAP = {

    # ========================================================
    # NEWS
    # ========================================================

    "aaj tak": "News",
    "aajtak": "News",
    "abp news": "News",
    "abp news hd": "News",
    "abp ananda": "News",
    "abp majha": "News",
    "abp asmita": "News",

    "india tv": "News",
    "india news": "News",
    "india news haryana": "News",

    "ndtv india": "News",
    "ndtv 24x7": "News",
    "ndtv bharat": "News",

    "news18 india": "News",
    "news18": "News",
    "news18 lokmat": "News",
    "news18 bangla": "News",
    "news18 assam": "News",
    "news18 odia": "News",
    "news18 punjab": "News",
    "news18 rajasthan": "News",
    "news18 up uk": "News",

    "zee news": "News",
    "zee news hd": "News",
    "zee 24 ghanta": "News",
    "zee 24 taas": "News",

    "times now": "News",
    "times now navbharat": "News",
    "times now world": "News",
    "mirror now": "News",

    "republic tv": "News",
    "republic bharat": "News",

    "india today": "News",
    "india today tv": "News",

    "wion": "News",

    "bbc news": "News",
    "bbc world news": "News",
    "bbc world": "News",

    "cnn": "News",
    "cnn international": "News",

    "al jazeera": "News",
    "aljazeera": "News",

    "news x": "News",
    "newsx": "News",

    "tv9 bharatvarsh": "News",
    "tv9 telugu": "News",
    "tv9 kannada": "News",
    "tv9 marathi": "News",

    "etv bharat": "News",
    "etv bharat hindi": "News",
    "etv bharat telangana": "News",
    "etv bharat andhra pradesh": "News",
    "etv bharat karnataka": "News",
    "etv bharat kerala": "News",
    "etv bharat tamil nadu": "News",

    # ========================================================
    # BUSINESS
    # ========================================================

    "cnbc tv18": "Business",
    "cnbc tv18 hd": "Business",
    "cnbc tv18 prime": "Business",
    "cnbc awaaz": "Business",

    "ndtv profit": "Business",
    "ndtv profit prime": "Business",

    "bloomberg": "Business",
    "bloomberg tv": "Business",

    "business today": "Business",
    "business news": "Business",

    "et now": "Business",
    "et now swadesh": "Business",

    "moneycontrol": "Business",

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

    "sony max": "Movies",
    "sony max hd": "Movies",
    "sony max 2": "Movies",

    "sony wah": "Movies",

    "movies now": "Movies",
    "movies now hd": "Movies",
    "mnx": "Movies",
    "mnx hd": "Movies",
    "romedy now": "Movies",

    "&pictures": "Movies",
    "and pictures": "Movies",

    "colors cineplex": "Movies",
    "colors cineplex hd": "Movies",

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
    "bhojpuri dhamaka": "Movies",

    # ========================================================
    # ENTERTAINMENT
    # ========================================================

    "zee tv": "Entertainment",
    "zee tv hd": "Entertainment",

    "star plus": "Entertainment",
    "star plus hd": "Entertainment",

    "star bharat": "Entertainment",
    "star bharat hd": "Entertainment",

    "colors": "Entertainment",
    "colors hd": "Entertainment",

    "&tv": "Entertainment",
    "and tv": "Entertainment",

    "sony entertainment television": "Entertainment",
    "sony entertainment television hd": "Entertainment",

    "sony sab": "Entertainment",
    "sony sab hd": "Entertainment",
    "sab tv": "Entertainment",

    "sony pal": "Entertainment",

    "star utsav": "Entertainment",

    "anmol tv": "Entertainment",

    "big magic": "Entertainment",

    "dangal": "Entertainment",
    "dangal 2": "Entertainment",

    "ishara": "Entertainment",

    "bindass": "Entertainment",
    "utv bindass": "Entertainment",

    "epic": "Infotainment",

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

    "vh1": "Music",
    "vh1 hd": "Music",

    "zing": "Music",

    "music india": "Music",
    "music zone": "Music",

    "dhamaka music": "Music",

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
    "cartoon network hd": "Kids",

    "pogo": "Kids",
    "pogo hd": "Kids",

    "nick": "Kids",
    "nick hd": "Kids",
    "nick jr": "Kids",
    "nickelodeon": "Kids",

    "sonic": "Kids",

    "disney": "Kids",
    "disney channel": "Kids",
    "disney junior": "Kids",

    "hungama": "Kids",
    "super hungama": "Kids",

    "discovery kids": "Kids",

    "etv bal bharat": "Kids",

    "cbeebies": "Kids",

    # ========================================================
    # SCIENCE
    # ========================================================

    "discovery science": "Science",
    "discovery science hd": "Science",

    "science channel": "Science",

    "nasa": "Science",
    "nasa tv": "Science",

    # ========================================================
    # LIFESTYLE
    # ========================================================

    "tlc": "Lifestyle",
    "tlc hd": "Lifestyle",

    "travelxp": "Lifestyle",
    "travel xp": "Lifestyle",

    "food food": "Lifestyle",

    "good times": "Lifestyle",

    "fashion tv": "Lifestyle",
    "fashiontv": "Lifestyle",

    # ========================================================
    # INFOTAINMENT
    # ========================================================

    "discovery channel": "Infotainment",
    "discovery hd": "Infotainment",

    "animal planet": "Infotainment",
    "animal planet hd": "Infotainment",

    "history tv": "Infotainment",
    "history": "Infotainment",

    "discovery turbo": "Infotainment",

    "discovery civilization": "Infotainment",

    "nat geo": "Infotainment",
    "nat geo hd": "Infotainment",
    "natgeo": "Infotainment",

    "national geographic": "Infotainment",

    "sony bbc earth": "Infotainment",
    "sony bbc earth hd": "Infotainment",

    "bbc earth": "Infotainment",

    "discovery world": "Infotainment",

    # ========================================================
    # SPORTS
    #
    # Cricket / Football / Hockey / Tennis
    # ALL GO INTO ONE GROUP: Sports
    # ========================================================

    # Cricket
    "star sports 1": "Sports",
    "star sports 1 hd": "Sports",
    "star sports 1 hindi": "Sports",
    "star sports 1 hindi hd": "Sports",

    "star sports 2": "Sports",
    "star sports 2 hd": "Sports",

    "star sports 3": "Sports",
    "star sports 3 hd": "Sports",

    "star sports first": "Sports",
    "star sports first hd": "Sports",

    "star sports khel": "Sports",
    "star sports khel hd": "Sports",

    "star sports tamil": "Sports",
    "star sports telugu": "Sports",
    "star sports kannada": "Sports",
    "star sports bangla": "Sports",

    "sony sports ten 1": "Sports",
    "sony sports ten 1 hd": "Sports",
    "sony ten 1": "Sports",

    "sony sports ten 2": "Sports",
    "sony sports ten 2 hd": "Sports",
    "sony ten 2": "Sports",

    "sony sports ten 3": "Sports",
    "sony sports ten 3 hd": "Sports",
    "sony ten 3": "Sports",

    "willow": "Sports",
    "willow cricket": "Sports",

    "dd sports": "Sports",

    # Football
    "sony sports ten 5": "Sports",
    "sony sports ten 5 hd": "Sports",
    "sony ten 5": "Sports",

    "bein sports": "Sports",
    "beinsports": "Sports",

    "football": "Sports",
    "football hd": "Sports",
    "soccer": "Sports",

    "premier league": "Sports",
    "champions league": "Sports",
    "uefa": "Sports",
    "fifa": "Sports",
    "la liga": "Sports",
    "bundesliga": "Sports",

    # Hockey
    "hockey": "Sports",
    "hockey india": "Sports",
    "star sports hockey": "Sports",

    # Tennis
    "tennis": "Sports",
    "tennis channel": "Sports",
    "sony sports ten 4": "Sports",
    "sony ten 4": "Sports",
    "atp": "Sports",
    "wta": "Sports",
    "wimbledon": "Sports",
    "roland garros": "Sports",

}


# ============================================================
# LANGUAGE DETECTION
# ============================================================

LANGUAGE_WORDS = {

    "Hindi": [
        "hindi",
        "bharat",
        "navbharat",
        "hind",
    ],

    "English": [
        "english",
        "bbc",
        "cnn",
        "bloomberg",
        "discovery",
        "animal planet",
        "national geographic",
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
        "ananda",
        "zee 24 ghanta",
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
# NORMALIZE
# ============================================================

def clean(value):

    if not value:
        return ""

    value = str(value).lower().strip()

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


# ============================================================
# EXTINF PARSER
# ============================================================

def parse_extinf(line):

    attrs = {}

    if "," in line:
        name = line.split(
            ",",
            1
        )[1].strip()
    else:
        name = ""

    matches = re.findall(
        r'([\w:-]+)="([^"]*)"',
        line
    )

    for key, value in matches:
        attrs[key.lower()] = value

    attrs["_name"] = name

    return attrs


# ============================================================
# CHANNEL NAME
# ============================================================

def get_channel_name(attrs):

    return (
        attrs.get("tvg-name")
        or attrs.get("tvg_name")
        or attrs.get("name")
        or attrs.get("_name")
        or ""
    ).strip()


# ============================================================
# EXACT / PARTIAL CHANNEL MATCH
# ============================================================

def find_channel_category(name):

    n = clean(name)

    if not n:
        return None

    # Exact match
    if n in CHANNEL_MAP:
        return CHANNEL_MAP[n]

    matches = []

    for channel, category in CHANNEL_MAP.items():

        key = clean(channel)

        if not key:
            continue

        if key in n:
            matches.append(
                (
                    len(key),
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
# SPORTS DETECTION
# ============================================================

def detect_sports(name, group=""):

    text = clean(
        name + " " + group
    )

    sports_words = [

        # Cricket
        "cricket",
        "star sports",
        "willow",
        "sony ten 1",
        "sony ten 2",
        "sony ten 3",
        "dd sports",

        # Football
        "football",
        "soccer",
        "premier league",
        "champions league",
        "uefa",
        "fifa",
        "la liga",
        "bundesliga",
        "bein sports",

        # Hockey
        "hockey",

        # Tennis
        "tennis",
        "atp",
        "wta",
        "wimbledon",
        "roland garros",
    ]

    for word in sports_words:

        if word in text:
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
# OLD GROUP CLASSIFICATION
# ============================================================

def old_group_category(group):

    g = clean(group)

    if not g:
        return None

    # NEVER use excluded categories
    for excluded in EXCLUDED_GROUPS:

        if excluded in g:
            return None

    aliases = {

        "news": "News",

        "entertainment": "Entertainment",

        "movie": "Movies",
        "movies": "Movies",
        "cinema": "Movies",

        "music": "Music",

        "kids": "Kids",
        "children": "Kids",

        "infotainment": "Infotainment",
        "knowledge": "Infotainment",

        "science": "Science",

        "lifestyle": "Lifestyle",

        "business": "Business",

        "sport": "Sports",
        "sports": "Sports",

    }

    for key, category in aliases.items():

        if key in g:
            return category

    return None


# ============================================================
# KEYWORD CLASSIFICATION
# ============================================================

def keyword_category(
    name,
    old_group
):

    text = clean(
        name + " " + old_group
    )

    # --------------------------------------------------------
    # EXCLUDED
    # --------------------------------------------------------

    excluded_words = [
        "regional",
        "devotional",
        "devotion",
        "bhakti",
        "spiritual",
        "education",
        "educational",
        "learning",
    ]

    for word in excluded_words:

        if word in text:
            return None

    # --------------------------------------------------------
    # SPORTS
    # --------------------------------------------------------

    sports = detect_sports(
        name,
        old_group
    )

    if sports:
        return "Sports"

    # --------------------------------------------------------
    # NEWS
    # --------------------------------------------------------

    if any(
        word in text
        for word in [
            "news",
            "breaking news",
            "times now",
            "republic",
            "aaj tak",
            "zee news",
            "abp news",
            "bbc news",
            "cnn",
            "al jazeera",
        ]
    ):
        return "News"

    # --------------------------------------------------------
    # BUSINESS
    # --------------------------------------------------------

    if any(
        word in text
        for word in [
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
    # KIDS
    # --------------------------------------------------------

    if any(
        word in text
        for word in [
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
    # MUSIC
    # --------------------------------------------------------

    if any(
        word in text
        for word in [
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
    # MOVIES
    # --------------------------------------------------------

    if any(
        word in text
        for word in [
            "movie",
            "movies",
            "cinema",
            "film",
            "films",
            "cineplex",
        ]
    ):
        return "Movies"

    # --------------------------------------------------------
    # SCIENCE
    # --------------------------------------------------------

    if any(
        word in text
        for word in [
            "science",
            "nasa",
        ]
    ):
        return "Science"

    # --------------------------------------------------------
    # LIFESTYLE
    # --------------------------------------------------------

    if any(
        word in text
        for word in [
            "lifestyle",
            "travel",
            "food",
            "fashion",
            "tlc",
        ]
    ):
        return "Lifestyle"

    # --------------------------------------------------------
    # INFOTAINMENT
    # --------------------------------------------------------

    if any(
        word in text
        for word in [
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
    # OLD SOURCE GROUP
    # --------------------------------------------------------

    return old_group_category(
        old_group
    )


# ============================================================
# FINAL CLASSIFICATION
# ============================================================

def classify(attrs):

    name = get_channel_name(
        attrs
    )

    old_group = (
        attrs.get(
            "group-title",
            ""
        )
        or attrs.get(
            "group",
            ""
        )
    )

    # --------------------------------------------------------
    # 1. Channel-name mapping
    # --------------------------------------------------------

    category = find_channel_category(
        name
    )

    # --------------------------------------------------------
    # 2. Sports ALWAYS wins
    # --------------------------------------------------------

    sports = detect_sports(
        name,
        old_group
    )

    if sports:
        category = "Sports"

    # --------------------------------------------------------
    # 3. Keyword fallback
    # --------------------------------------------------------

    if not category:

        category = keyword_category(
            name,
            old_group
        )

    # --------------------------------------------------------
    # 4. Excluded category protection
    # --------------------------------------------------------

    if category:

        if clean(category) in EXCLUDED_GROUPS:

            category = None

    # --------------------------------------------------------
    # 5. Only allowed groups
    # --------------------------------------------------------

    if category not in ALLOWED_GROUPS:

        category = "Entertainment"

    # --------------------------------------------------------
    # LANGUAGE
    # --------------------------------------------------------

    language = detect_language(
        name,
        old_group,
        attrs
    )

    return language, category


# ============================================================
# EXTINF REWRITE
# ============================================================

def rewrite_extinf(entry):

    line = entry["extinf"]

    attrs = entry["attrs"]

    language, category = classify(
        attrs
    )

    # --------------------------------------------------------
    # REMOVE OLD GROUP
    # --------------------------------------------------------

    line = re.sub(
        r'\s*group-title="[^"]*"',
        "",
        line,
        flags=re.I
    )

    # Some playlists use group-title without quotes
    line = re.sub(
        r"\s*group-title=[^\s,]+",
        "",
        line,
        flags=re.I
    )

    # --------------------------------------------------------
    # NEW GROUP
    # --------------------------------------------------------

    line = (
        line.rstrip()
        + f' group-title="{category}"'
    )

    # --------------------------------------------------------
    # LANGUAGE METADATA
    # --------------------------------------------------------

    if language != "Unknown":

        line = re.sub(
            r'\s*tvg-language="[^"]*"',
            "",
            line,
            flags=re.I
        )

        line = re.sub(
            r"\s*tvg-language=[^\s,]+",
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
# M3U PARSER
# ============================================================

def parse_m3u(path):

    entries = []

    with open(
        path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as f:

        lines = [
            line.rstrip("\r\n")
            for line in f
        ]

    current = None

    for line in lines:

        # New channel
        if line.startswith("#EXTINF:"):

            current = {
                "extinf": line,
                "attrs": parse_extinf(line),
                "url": "",
            }

            continue

        # URL line
        if (
            current
            and line.strip()
            and not line.startswith("#")
        ):

            current["url"] = line.strip()

            entries.append(
                current
            )

            current = None

    return entries


# ============================================================
# BUILD PLAYLIST
# ============================================================

def build_playlist(
    source,
    output
):

    files = sorted(
        glob.glob(
            os.path.join(
                source,
                "**",
                "*.m3u"
            ),
            recursive=True
        )
    )

    if not files:

        print(
            "ERROR: No .m3u files found in:",
            source
        )

        sys.exit(1)

    all_entries = []

    print()
    print(
        "=========================================="
    )
    print(
        " IPTV PLAYLIST GROUP BUILDER"
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
    # Read every playlist
    # --------------------------------------------------------

    for path in files:

        print(
            "Reading:",
            path
        )

        try:

            entries = parse_m3u(
                path
            )

            all_entries.extend(
                entries
            )

            print(
                "  Streams:",
                len(entries)
            )

        except Exception as e:

            print(
                "  ERROR:",
                e
            )

    print()
    print(
        "TOTAL SOURCE STREAMS:",
        len(all_entries)
    )

    # --------------------------------------------------------
    # IMPORTANT:
    #
    # NO DEDUPLICATION
    #
    # Same channel
    # Different URL
    #
    # Both stay.
    # --------------------------------------------------------

    output_dir = os.path.dirname(
        os.path.abspath(output)
    )

    if output_dir:
        os.makedirs(
            output_dir,
            exist_ok=True
        )

    # --------------------------------------------------------
    # GROUP COUNTERS
    # --------------------------------------------------------

    counters = {}

    for entry in all_entries:

        try:

            language, category = classify(
                entry["attrs"]
            )

            counters[category] = (
                counters.get(
                    category,
                    0
                ) + 1
            )

        except Exception:
            pass

    # --------------------------------------------------------
    # WRITE PLAYLIST
    # --------------------------------------------------------

    with open(
        output,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            '#EXTM3U '
            'x-tvg-url="guide.xml.gz"\n'
        )

        written = 0

        for entry in all_entries:

            url = entry.get(
                "url",
                ""
            ).strip()

            if not url:
                continue

            try:

                extinf = rewrite_extinf(
                    entry
                )

            except Exception as e:

                print(
                    "Classification error:",
                    e
                )

                continue

            f.write(
                extinf + "\n"
            )

            f.write(
                url + "\n"
            )

            written += 1

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    print()
    print(
        "=========================================="
    )
    print(
        " BUILD COMPLETE"
    )
    print(
        "=========================================="
    )

    print(
        "Output:",
        os.path.abspath(output)
    )

    print(
        "Streams written:",
        written
    )

    print()
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
            f"  {group}:",
            counters.get(
                group,
                0
            )
        )

    print()
    print(
        "EXCLUDED:"
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

    print()
    print(
        "SPORTS:"
    )

    print(
        "  Cricket -> Sports"
    )

    print(
        "  Football -> Sports"
    )

    print(
        "  Hockey -> Sports"
    )

    print(
        "  Tennis -> Sports"
    )

    print()
    print(
        "DUPLICATES:"
    )

    print(
        "  KEPT - no URL deduplication"
    )

    print(
        "=========================================="
    )


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Group IPTV M3U channels "
            "without removing duplicate streams"
        )
    )

    parser.add_argument(
        "source",
        help=(
            "Directory containing "
            "source M3U playlists"
        )
    )

    parser.add_argument(
        "-o",
        "--output",
        default="playlist.m3u",
        help=(
            "Output playlist path"
        )
    )

    args = parser.parse_args()

    source = os.path.abspath(
        args.source
    )

    if not os.path.isdir(source):

        print(
            "ERROR: Source directory does not exist:"
        )

        print(
            source
        )

        sys.exit(1)

    build_playlist(
        source,
        args.output
    )


if __name__ == "__main__":

    main()
