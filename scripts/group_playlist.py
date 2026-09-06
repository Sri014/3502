#!/usr/bin/env python3

import argparse
import html
import re
import ssl
import urllib.request
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import urlparse


# ============================================================
# FINAL CONFIG
# ============================================================

ALLOWED_CATEGORIES = [
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

EXCLUDED_WORDS = (
    "regional",
    "devotional",
    "spiritual",
    "education",
)

ALLOWED_LANGUAGES = {
    "hindi": "Hindi",
    "hin": "Hindi",
    "english": "English",
    "eng": "English",
    "bhojpuri": "Bhojpuri",
}

REGIONAL_LANGUAGES = {
    "bengali",
    "bangla",
    "tamil",
    "telugu",
    "kannada",
    "malayalam",
    "marathi",
    "punjabi",
    "gujarati",
    "odia",
    "oriya",
    "assamese",
    "nepali",
    "sinhala",
}

SPORT_WORDS = (
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
    "formula 1",
    "f1",
    "motogp",
    "golf",
    "boxing",
    "wrestling",
)

CRICKET_WORDS = (
    "cricket",
    "ipl",
    "t20",
    "test cricket",
    "odi cricket",
)

# Names that are too generic for fuzzy matching.
GENERIC_NAMES = {
    "news",
    "music",
    "movies",
    "sports",
    "entertainment",
    "live",
    "channel",
    "tv",
}


# ============================================================
# WEB REFERENCE SOURCES
#
# Streams NEVER come from these websites.
# They are ONLY used to identify Indian channel names.
# ============================================================

REFERENCE_URLS = [
    # Tata Play official
    "https://www.tataplay.com/channels/tv-channel-number-list",

    # Airtel official
    "https://www.airtel.in/plans/dth/all-channel-list",

    # JioTV public channel list
    "https://www.ytechb.com/jiotv-plus-channel-list-numbers-plans/",
]


# ============================================================
# FALLBACK REFERENCE CHANNELS
#
# Used if one of the websites changes its HTML.
# ============================================================

FALLBACK_CHANNELS = {
    # NEWS
    "aaj tak",
    "aaj tak hd",
    "india today",
    "ndtv india",
    "ndtv",
    "ndtv 24x7",
    "news18 india",
    "news 18 india",
    "cnn news18",
    "zee news",
    "zee hindustan",
    "india tv",
    "news24",
    "news 24",
    "republic tv",
    "republic bharat",
    "tv9 bharatvarsh",
    "abp news",
    "good news today",
    "india news",
    "bharat 24",
    "bharat express",
    "news nation",
    "times now",
    "times now navbharat",
    "wion",
    "firstpost",
    "sansad tv",
    "dd news",
    "dd india",
    "cnbc awaaz",
    "zee business",
    "et now",
    "et now swadesh",

    # ENTERTAINMENT
    "star plus",
    "star plus hd",
    "star bharat",
    "star utsav",
    "sony",
    "sony hd",
    "sony entertainment",
    "sony entertainment television",
    "sony sab",
    "sony sab hd",
    "sony pal",
    "&tv",
    "&tv hd",
    "colors",
    "colors hd",
    "zee tv",
    "zee tv hd",
    "zee anmol",
    "dangal",
    "big magic",
    "shemaroo tv",
    "shemaroo umang",
    "sony aath",
    "zee zindagi",
    "and tv",

    # MOVIES
    "sony max",
    "sony max hd",
    "sony max 2",
    "sony wah",
    "zee cinema",
    "zee cinema hd",
    "zee classic",
    "zee bollywood",
    "zee anmol cinema",
    "star gold",
    "star gold hd",
    "star gold select",
    "colors cineplex",
    "colors cineplex hd",
    "colors cineplex superhit",
    "colors cineplex superhits",
    "&pictures",
    "&pictures hd",
    "b4u movies",
    "b4u cinema",
    "b4u kadak",
    "goldmines",
    "goldmines bollywood",
    "manoranjan tv",
    "manoranjan grand",
    "filamchi",
    "wow cinema",
    "dhamaal tv",

    # MUSIC
    "b4u music",
    "9xm",
    "9x music",
    "9x jhakaas",
    "9x tashan",
    "mtv",
    "mtv hd",
    "mtv beats",
    "zoom",
    "mastiii",
    "music india",
    "zing",
    "vh1",
    "sony mix",

    # KIDS
    "cartoon network",
    "cartoon network hindi",
    "pogo",
    "hungama",
    "hungama tv",
    "discovery kids",
    "sony yay",
    "nick",
    "nick hd",
    "nick jr",
    "sonic",
    "super hungama",
    "disney channel",
    "disney junior",

    # BUSINESS
    "cnbc tv18",
    "cnbc tv18 hd",
    "cnbc awaaz",
    "ndtv profit",
    "business today",
    "zee business",
    "et now",
    "et now swadesh",

    # SPORTS
    "star sports",
    "star sports 1",
    "star sports 2",
    "star sports 1 hindi",
    "star sports 2 hindi",
    "star sports select 1",
    "star sports select 2",
    "star sports select 1 hd",
    "star sports select 2 hd",
    "sony sports",
    "sony sports ten 1",
    "sony sports ten 2",
    "sony sports ten 3",
    "sony sports ten 4",
    "sony sports ten 5",
    "sony ten 1",
    "sony ten 2",
    "sony ten 3",
    "sony ten 4",
    "sony ten 5",
    "sports18",
    "sports18 1",
    "sports18 2",
    "sports18 khel",
    "dd sports",
    "eurosport",

    # INFOTAINMENT / SCIENCE
    "discovery",
    "discovery channel",
    "discovery hd",
    "discovery hd world",
    "animal planet",
    "animal planet hd",
    "history tv18",
    "history tv 18",
    "history tv18 hd",
    "epic",
    "epic tv",
    "national geographic",
    "national geographic channel",
    "nat geo",
    "nat geo hd",
    "nat geo wild",
    "nat geo wild hd",
    "discovery science",
    "discovery turbo",

    # LIFESTYLE
    "travel xp",
    "travelxp",
    "food food",
    "living foodz",
    "fashion tv",
    "tlc",
}


# ============================================================
# CATEGORY MAP
# ============================================================

CATEGORY_KEYWORDS = {
    "Sports": (
        "sports",
        "sport",
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
    ),

    "News": (
        "news",
        "aaj tak",
        "ndtv",
        "abp",
        "republic",
        "india news",
        "news18",
        "times now",
        "wion",
        "firstpost",
        "bharat express",
        "bharat 24",
        "sansad",
    ),

    "Business": (
        "cnbc",
        "business",
        "profit",
        "et now",
        "finance",
        "bloomberg",
    ),

    "Movies": (
        "movie",
        "movies",
        "cinema",
        "cineplex",
        "max",
        "pictures",
        "bollywood",
        "goldmines",
        "filamchi",
        "manoranjan",
        "shemaroo",
        "b4u movies",
    ),

    "Music": (
        "music",
        "mtv",
        "9xm",
        "9x",
        "mastiii",
        "zoom",
        "zing",
        "vh1",
        "sony mix",
    ),

    "Kids": (
        "cartoon",
        "kids",
        "pogo",
        "hungama",
        "nick",
        "sonic",
        "sony yay",
        "disney junior",
        "disney channel",
        "super hungama",
    ),

    "Science": (
        "science",
        "nat geo",
        "national geographic",
        "discovery science",
        "discovery turbo",
    ),

    "Infotainment": (
        "discovery",
        "animal planet",
        "history tv",
        "history",
        "epic",
        "documentary",
    ),

    "Lifestyle": (
        "travel",
        "travelxp",
        "travel xp",
        "food food",
        "food",
        "living foodz",
        "fashion tv",
        "tlc",
        "lifestyle",
    ),

    "Entertainment": (
        "star plus",
        "star bharat",
        "star utsav",
        "sony",
        "sab",
        "zee tv",
        "zee anmol",
        "colors",
        "dangal",
        "big magic",
        "entertainment",
        "&tv",
    ),
}


# ============================================================
# HTTP
# ============================================================

def fetch_url(url):
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(X11; Linux x86_64) "
                    "AppleWebKit/537.36 "
                    "Chrome/130 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml",
            },
        )

        context = ssl.create_default_context()

        with urllib.request.urlopen(
            req,
            timeout=30,
            context=context,
        ) as response:
            return response.read().decode(
                "utf-8",
                errors="ignore",
            )

    except Exception as e:
        print(f"REFERENCE WARNING: {url}")
        print(f"  {e}")
        return ""


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def clean(value):
    if value is None:
        return ""

    value = html.unescape(str(value))

    value = value.replace("&amp;", "&")

    value = re.sub(
        r"\b(HD|SD|FHD|UHD|4K|2K|PLUS)\b",
        " ",
        value,
        flags=re.I,
    )

    value = re.sub(
        r"[^a-zA-Z0-9&]+",
        " ",
        value,
    )

    value = re.sub(
        r"\s+",
        " ",
        value,
    )

    return value.strip()


def normalize(value):
    value = clean(value).lower()

    replacements = {
        "sony entertainment television": "sony",
        "sony entertainment": "sony",
        "zee tv hd": "zee tv",
        "sony sab hd": "sony sab",
        "star plus hd": "star plus",
        "colors hd": "colors",
        "star bharat hd": "star bharat",
        "history tv 18": "history tv18",
        "cnn news 18": "cnn news18",
        "news 18": "news18",
    }

    for old, new in replacements.items():
        value = value.replace(old, new)

    value = re.sub(
        r"\s+",
        " ",
        value,
    )

    return value.strip()


def tokens(value):
    return {
        x
        for x in normalize(value).split()
        if len(x) > 1
    }


# ============================================================
# REFERENCE NAME EXTRACTION
# ============================================================

def extract_reference_names(page):
    names = set()

    if not page:
        return names

    page = html.unescape(page)

    # Table cells / headings / common channel-name fields.
    patterns = [
        r"<td[^>]*>\s*([^<]{2,100})\s*</td>",
        r"<th[^>]*>\s*([^<]{2,100})\s*</th>",
        r"<h[1-6][^>]*>\s*([^<]{2,100})\s*</h[1-6]>",
        r'"channelName"\s*:\s*"([^"]{2,100})"',
        r'"channel_name"\s*:\s*"([^"]{2,100})"',
        r'"name"\s*:\s*"([^"]{2,100})"',
    ]

    for pattern in patterns:
        for match in re.findall(
            pattern,
            page,
            flags=re.I,
        ):
            value = clean(match)

            if not value:
                continue

            n = normalize(value)

            if len(n) < 3:
                continue

            if n in GENERIC_NAMES:
                continue

            if any(
                word in n
                for word in (
                    "channel number",
                    "channel name",
                    "price",
                    "language",
                    "quality",
                    "monthly",
                    "subscription",
                    "search for",
                    "load more",
                )
            ):
                continue

            # Ignore obvious UI text.
            if len(n.split()) > 10:
                continue

            names.add(n)

    return names


def load_reference_channels():
    references = set()

    print()
    print("========================================")
    print(" BUILDING INDIAN CHANNEL REFERENCE")
    print("========================================")

    for url in REFERENCE_URLS:
        page = fetch_url(url)

        found = extract_reference_names(page)

        print(
            f"REFERENCE: {url}"
        )
        print(
            f"  CHANNEL NAMES FOUND: {len(found)}"
        )

        references.update(found)

    # Always keep fallback names.
    for name in FALLBACK_CHANNELS:
        references.add(normalize(name))

    print(
        f"TOTAL REFERENCE NAMES: {len(references)}"
    )

    return references


# ============================================================
# M3U PARSER
# ============================================================

def parse_extinf(line):
    attrs = {}

    match = re.match(
        r"#EXTINF:[^ ]*(?:\s+(.*))?,(.*)$",
        line,
    )

    if not match:
        return attrs, ""

    attribute_text = match.group(1) or ""
    name = clean(match.group(2))

    pattern = re.compile(
        r'([\w-]+)="([^"]*)"'
    )

    for key, value in pattern.findall(
        attribute_text
    ):
        attrs[key.lower()] = html.unescape(
            value.strip()
        )

    return attrs, name


def parse_m3u(path):
    entries = []

    try:
        lines = Path(path).read_text(
            encoding="utf-8",
            errors="ignore",
        ).splitlines()

    except Exception as e:
        print(
            f"WARNING: cannot read {path}: {e}"
        )
        return entries

    pending_attrs = None
    pending_name = None

    for raw in lines:
        line = raw.strip()

        if not line:
            continue

        if line.startswith("#EXTINF:"):
            pending_attrs, pending_name = (
                parse_extinf(line)
            )
            continue

        if line.startswith("#"):
            continue

        if pending_attrs is None:
            continue

        url = line.strip()

        if url.startswith(
            ("http://", "https://")
        ):
            entries.append({
                "attrs": pending_attrs,
                "name": pending_name or "",
                "url": url,
                "source": str(path),
            })

        pending_attrs = None
        pending_name = None

    return entries


# ============================================================
# CHANNEL NAME MATCHING
# ============================================================

def similarity(a, b):
    a = normalize(a)
    b = normalize(b)

    if not a or not b:
        return 0.0

    if a == b:
        return 1.0

    # One is exact token subset of the other.
    ta = tokens(a)
    tb = tokens(b)

    if ta and tb:
        common = len(ta & tb)
        union = len(ta | tb)

        if common >= 2:
            score = common / union

            if score >= 0.70:
                return max(
                    score,
                    SequenceMatcher(
                        None,
                        a,
                        b,
                    ).ratio(),
                )

    return SequenceMatcher(
        None,
        a,
        b,
    ).ratio()


def find_reference_match(name, references):
    n = normalize(name)

    if not n:
        return False, "", 0.0

    if n in references:
        return True, n, 1.0

    # Strong substring match.
    for ref in references:
        if len(ref) < 5:
            continue

        if n == ref:
            return True, ref, 1.0

        if (
            len(n) >= 7
            and (
                n in ref
                or ref in n
            )
        ):
            return True, ref, 0.94

    # Fuzzy matching.
    best_ref = ""
    best_score = 0.0

    for ref in references:
        if len(ref) < 5:
            continue

        score = similarity(
            n,
            ref,
        )

        if score > best_score:
            best_score = score
            best_ref = ref

    # Conservative threshold.
    if best_score >= 0.88:
        return True, best_ref, best_score

    return False, best_ref, best_score


# ============================================================
# LANGUAGE
# ============================================================

def detect_language(
    attrs,
    name,
    group,
    source,
):
    values = [
        attrs.get("tvg-language", ""),
        attrs.get("language", ""),
        name,
        group,
        Path(source).name,
    ]

    text = " ".join(
        normalize(x)
        for x in values
    )

    # Explicit regional language = reject.
    for lang in REGIONAL_LANGUAGES:
        if re.search(
            r"\b" + re.escape(lang) + r"\b",
            text,
        ):
            return "REGIONAL"

    # Hindi.
    if re.search(
        r"\bhindi\b|\bhin\b",
        text,
    ):
        return "Hindi"

    # Bhojpuri.
    if "bhojpuri" in text:
        return "Bhojpuri"

    # English.
    if re.search(
        r"\benglish\b|\beng\b",
        text,
    ):
        return "English"

    # Source playlist itself is a useful language hint.
    filename = Path(source).name.lower()

    if "hindi" in filename:
        return "Hindi"

    if "english" in filename:
        return "English"

    # Known Indian channels where language is obvious.
    n = normalize(name)

    hindi_indicators = (
        "aaj tak",
        "zee hindi",
        "star plus",
        "star bharat",
        "sony sab",
        "zee tv",
        "colors",
        "dangal",
        "sony pal",
        "zee anmol",
        "b4u kadak",
        "b4u movies",
        "star gold",
        "zee cinema",
        "sony max",
    )

    if any(
        x in n
        for x in hindi_indicators
    ):
        return "Hindi"

    # English Indian feeds.
    english_indicators = (
        "ndtv 24x7",
        "ndtv",
        "cnbc tv18",
        "cnbc",
        "india today",
        "cnn news18",
        "firstpost",
        "wion",
        "et now",
        "discovery",
        "animal planet",
        "national geographic",
        "nat geo",
        "history tv",
        "travel xp",
        "fashion tv",
        "tlc",
    )

    if any(
        x in n
        for x in english_indicators
    ):
        return "English"

    return ""


# ============================================================
# SPORT
# ============================================================

def is_sport(
    attrs,
    name,
    group,
    url,
):
    text = " ".join([
        normalize(
            attrs.get(
                "group-title",
                "",
            )
        ),
        normalize(
            attrs.get(
                "tvg-name",
                "",
            )
        ),
        normalize(name),
        normalize(group),
        normalize(url),
    ])

    return any(
        word in text
        for word in SPORT_WORDS
    )


def is_cricket(
    attrs,
    name,
    group,
    url,
):
    text = " ".join([
        normalize(
            attrs.get(
                "group-title",
                "",
            )
        ),
        normalize(name),
        normalize(group),
        normalize(url),
    ])

    return any(
        word in text
        for word in CRICKET_WORDS
    )


# ============================================================
# CATEGORY
# ============================================================

def category_from_text(
    attrs,
    name,
    group,
):
    text = " ".join([
        normalize(
            attrs.get(
                "group-title",
                "",
            )
        ),
        normalize(name),
        normalize(group),
    ])

    # Sports first.
    if any(
        x in text
        for x in CATEGORY_KEYWORDS["Sports"]
    ):
        return "Sports"

    # Exact group from source.
    group_lower = normalize(group)

    for category in ALLOWED_CATEGORIES:
        if group_lower == category.lower():
            return category

    # Keyword category.
    for category in ALLOWED_CATEGORIES:
        if category == "Sports":
            continue

        for keyword in CATEGORY_KEYWORDS[
            category
        ]:
            if keyword in text:
                return category

    return None


def classify(
    attrs,
    name,
    group,
):
    # Never allow excluded source groups.
    g = normalize(group)

    if any(
        x in g
        for x in EXCLUDED_WORDS
    ):
        return None

    return category_from_text(
        attrs,
        name,
        group,
    )


# ============================================================
# INDIAN / CRICKET FILTER
# ============================================================

def allowed_entry(
    entry,
    references,
):
    attrs = entry["attrs"]
    name = entry["name"]
    url = entry["url"]
    source = entry["source"]

    group = attrs.get(
        "group-title",
        "",
    )

    sport = is_sport(
        attrs,
        name,
        group,
        url,
    )

    cricket = is_cricket(
        attrs,
        name,
        group,
        url,
    )

    # --------------------------------------------------------
    # CRICKET FROM ANY COUNTRY IS ALLOWED
    # --------------------------------------------------------

    if cricket:
        return True, "CRICKET"

    # --------------------------------------------------------
    # MATCH CHANNEL AGAINST JIO / TATA / AIRTEL
    # --------------------------------------------------------

    matched, matched_name, score = (
        find_reference_match(
            name,
            references,
        )
    )

    if not matched:
        # Try tvg-name.
        tvg_name = attrs.get(
            "tvg-name",
            "",
        )

        if tvg_name:
            matched, matched_name, score = (
                find_reference_match(
                    tvg_name,
                    references,
                )
            )

    if not matched:
        return False, "NOT_IN_INDIAN_REFERENCE"

    # --------------------------------------------------------
    # LANGUAGE FILTER
    # --------------------------------------------------------

    language = detect_language(
        attrs,
        name,
        group,
        source,
    )

    if language == "REGIONAL":
        return False, "REGIONAL_LANGUAGE"

    # If explicitly known language, enforce it.
    if language:
        if language not in (
            "Hindi",
            "English",
            "Bhojpuri",
        ):
            return False, "OTHER_LANGUAGE"

    # --------------------------------------------------------
    # INDIAN CHANNEL MATCHED
    #
    # Country of stream DOES NOT MATTER.
    # USA / UK / Middle East / Australia etc. allowed.
    # --------------------------------------------------------

    return True, (
        f"INDIAN_MATCH:{matched_name}:{score:.3f}"
    )


# ============================================================
# EXTINF
# ============================================================

def rewrite_extinf(
    attrs,
    name,
    category,
    language,
):
    new_attrs = dict(attrs)

    new_attrs["group-title"] = category

    if language in (
        "Hindi",
        "English",
        "Bhojpuri",
    ):
        new_attrs[
            "tvg-language"
        ] = language

    preferred = [
        "tvg-id",
        "tvg-name",
        "tvg-logo",
        "tvg-language",
        "tvg-country",
        "group-title",
    ]

    parts = []
    used = set()

    for key in preferred:
        value = new_attrs.get(
            key,
            "",
        )

        if value:
            parts.append(
                f'{key}="{value}"'
            )
            used.add(key)

    for key, value in new_attrs.items():
        if key in used:
            continue

        if not value:
            continue

        parts.append(
            f'{key}="{value}"'
        )

    return (
        "#EXTINF:-1 "
        + " ".join(parts)
        + ","
        + name
    )


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Indian IPTV playlist builder "
            "using JioTV/Tata Play/Airtel "
            "channel-name matching."
        )
    )

    parser.add_argument(
        "source",
        help="Directory containing M3U/M3U8 files",
    )

    parser.add_argument(
        "-o",
        "--output",
        default="playlist.m3u",
    )

    args = parser.parse_args()

    source_dir = Path(
        args.source
    )

    if not source_dir.exists():
        raise SystemExit(
            f"ERROR: source directory not found: "
            f"{source_dir}"
        )

    # Recursive scan.
    files = sorted(
        p
        for p in source_dir.rglob("*")
        if p.is_file()
        and p.suffix.lower()
        in (
            ".m3u",
            ".m3u8",
        )
    )

    if not files:
        raise SystemExit(
            "ERROR: no M3U/M3U8 files found."
        )

    print(
        "========================================"
    )
    print(
        " IPTV PLAYLIST GENERATOR"
    )
    print(
        "========================================"
    )

    print(
        f"M3U FILES FOUND: {len(files)}"
    )

    for path in files:
        print(
            " -",
            path,
        )

    # --------------------------------------------------------
    # BUILD REFERENCE
    # --------------------------------------------------------

    references = (
        load_reference_channels()
    )

    # --------------------------------------------------------
    # READ ALL PLAYLISTS
    # --------------------------------------------------------

    all_entries = []

    for path in files:
        entries = parse_m3u(path)

        print(
            f"{path.name}: "
            f"{len(entries)} entries"
        )

        all_entries.extend(
            entries
        )

    print()
    print(
        f"TOTAL SOURCE ENTRIES: "
        f"{len(all_entries)}"
    )

    # --------------------------------------------------------
    # FILTER
    # --------------------------------------------------------

    final_entries = []

    seen_urls = set()

    stats = {
        "cricket": 0,
        "indian": 0,
        "not_reference": 0,
        "regional": 0,
        "other_language": 0,
        "uncategorized": 0,
        "duplicate": 0,
    }

    for entry in all_entries:
        attrs = entry["attrs"]
        name = entry["name"]
        url = entry["url"]
        source = entry["source"]

        group = attrs.get(
            "group-title",
            "",
        )

        # Exact URL duplicate.
        if url in seen_urls:
            stats["duplicate"] += 1
            continue

        allowed, reason = allowed_entry(
            entry,
            references,
        )

        if not allowed:
            if (
                reason
                == "NOT_IN_INDIAN_REFERENCE"
            ):
                stats["not_reference"] += 1

            elif (
                reason
                == "REGIONAL_LANGUAGE"
            ):
                stats["regional"] += 1

            elif (
                reason
                == "OTHER_LANGUAGE"
            ):
                stats["other_language"] += 1

            continue

        if reason == "CRICKET":
            stats["cricket"] += 1
        else:
            stats["indian"] += 1

        category = classify(
            attrs,
            name,
            group,
        )

        # Cricket always belongs to Sports.
        if is_cricket(
            attrs,
            name,
            group,
            url,
        ):
            category = "Sports"

        if not category:
            stats["uncategorized"] += 1
            continue

        if category not in ALLOWED_CATEGORIES:
            stats["uncategorized"] += 1
            continue

        language = detect_language(
            attrs,
            name,
            group,
            source,
        )

        # If no explicit language is detected,
        # keep it because the Indian reference
        # matched and the source playlist itself
        # may not expose language metadata.
        #
        # Regional was already rejected above.

        seen_urls.add(url)

        extinf = rewrite_extinf(
            attrs,
            name,
            category,
            language,
        )

        final_entries.append({
            "extinf": extinf,
            "url": url,
            "category": category,
            "name": name,
            "language": language,
        })

    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    category_order = {
        category: index
        for index, category
        in enumerate(
            ALLOWED_CATEGORIES,
            start=1,
        )
    }

    final_entries.sort(
        key=lambda x: (
            category_order.get(
                x["category"],
                999,
            ),
            x["language"],
            x["name"].lower(),
            x["url"],
        )
    )

    # --------------------------------------------------------
    # WRITE
    # --------------------------------------------------------

    output = Path(
        args.output
    )

    with output.open(
        "w",
        encoding="utf-8",
        newline="\n",
    ) as f:

        f.write(
            '#EXTM3U '
            'x-tvg-url="'
            'https://raw.githubusercontent.com/'
            'Sri014/3502/main/epg.xml'
            '"\n'
        )

        for entry in final_entries:
            f.write(
                entry["extinf"]
                + "\n"
            )

            f.write(
                entry["url"]
                + "\n"
            )

    # --------------------------------------------------------
    # FINAL STATS
    # --------------------------------------------------------

    counts = {
        category: 0
        for category
        in ALLOWED_CATEGORIES
    }

    for entry in final_entries:
        counts[
            entry["category"]
        ] += 1

    print()
    print(
        "========================================"
    )
    print(
        " FINAL RESULT"
    )
    print(
        "========================================"
    )

    print(
        f"FINAL CHANNELS: "
        f"{len(final_entries)}"
    )

    print(
        f"INDIAN MATCHED: "
        f"{stats['indian']}"
    )

    print(
        f"CRICKET ALLOWED: "
        f"{stats['cricket']}"
    )

    print(
        f"NOT IN INDIAN REFERENCE: "
        f"{stats['not_reference']}"
    )

    print(
        f"REGIONAL LANGUAGE REMOVED: "
        f"{stats['regional']}"
    )

    print(
        f"OTHER LANGUAGE REMOVED: "
        f"{stats['other_language']}"
    )

    print(
        f"UNCATEGORIZED: "
        f"{stats['uncategorized']}"
    )

    print(
        f"DUPLICATE URL REMOVED: "
        f"{stats['duplicate']}"
    )

    print()
    print("GROUPS:")

    for category in ALLOWED_CATEGORIES:
        print(
            f"  {category}: "
            f"{counts[category]}"
        )

    print()
    print(
        f"OUTPUT: {output}"
    )


if __name__ == "__main__":
    main()
