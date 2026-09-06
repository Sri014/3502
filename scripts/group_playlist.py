#!/usr/bin/env python3

import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

# ============================================================
# CONFIG
# ============================================================

SOURCE_URLS = [
    "https://raw.githubusercontent.com/wizakorhd/iptv/refs/heads/main/playlist-hindi.m3u",
    "https://raw.githubusercontent.com/wizakorhd/iptv/refs/heads/main/playlist-english-india.m3u",
    "https://raw.githubusercontent.com/wizakorhd/iptv/refs/heads/main/playlist-top.m3u",
    "https://raw.githubusercontent.com/wizakorhd/iptv/refs/heads/main/playlist.m3u",
]

ALLOWED_GROUPS = [
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

ALLOWED_LANGUAGES = {"hindi", "english", "bhojpuri"}

# Explicitly unwanted regional languages.
OTHER_REGIONAL_LANGUAGES = {
    "bengali", "bangla",
    "tamil",
    "telugu",
    "kannada",
    "malayalam",
    "marathi",
    "punjabi",
    "gujarati",
    "odia", "oriya",
    "assamese",
    "nepali",
    "sinhala",
    "urdu",
    "konkani",
    "manipuri",
    "meitei",
    "sindhi",
    "kashmiri",
    "dogri",
    "maithili",
    "rajasthani",
    "haryanvi",
    "chhattisgarhi",
}

# ============================================================
# CHANNEL -> JioTV STYLE GROUP
# Source repo group-title is NEVER trusted.
# ============================================================

CHANNEL_GROUPS = {
    # ---------------- NEWS ----------------
    "aaj tak": "News",
    "abp news": "News",
    "abp ananda": "News",
    "bbc news": "News",
    "bbc news hd": "News",
    "cnn": "News",
    "cnn news18": "News",
    "cnn-news18": "News",
    "news18": "News",
    "news18 india": "News",
    "news18 delhi": "News",
    "news18 bihar": "News",
    "news18 up": "News",
    "news18 rajasthan": "News",
    "news18 mp": "News",
    "news18 urdu": "News",
    "ndtv": "News",
    "ndtv india": "News",
    "ndtv 24x7": "News",
    "india today": "News",
    "india tv": "News",
    "times now": "News",
    "times now navbharat": "News",
    "mirror now": "News",
    "news nation": "News",
    "news24": "News",
    "news 24": "News",
    "republic bharat": "News",
    "republic tv": "News",
    "republic world": "News",
    "zee news": "News",
    "zee business": "Business",
    "zee media": "News",
    "zee news hd": "News",
    "tezz": "News",
    "good news today": "News",
    "firstpost": "News",
    "newsx": "News",
    "wion": "News",
    "al jazeera": "News",
    "dw": "News",
    "euronews": "News",
    "nhk world": "News",

    # ---------------- BUSINESS ----------------
    "cnbc tv18": "Business",
    "cnbc tv18 prime": "Business",
    "cnbc awaaz": "Business",
    "cnbc": "Business",
    "et now": "Business",
    "et now swadesh": "Business",
    "bloomberg": "Business",
    "business today": "Business",
    "moneycontrol": "Business",
    "zee business": "Business",

    # ---------------- ENTERTAINMENT ----------------
    "star plus": "Entertainment",
    "star bharat": "Entertainment",
    "star utsav": "Entertainment",
    "star utsav movies": "Movies",
    "sony entertainment television": "Entertainment",
    "sony entertainment": "Entertainment",
    "sony sab": "Entertainment",
    "sony pal": "Entertainment",
    "sony aath": "Entertainment",
    "colors": "Entertainment",
    "colors tv": "Entertainment",
    "colors rishtey": "Entertainment",
    "colors cineplex": "Movies",
    "colors cineplex superhits": "Movies",
    "zee tv": "Entertainment",
    "zee anmol": "Entertainment",
    "zee anmol cinema": "Movies",
    "&tv": "Entertainment",
    "and tv": "Entertainment",
    "and picture": "Movies",
    "&pictures": "Movies",
    "andpictures": "Movies",
    "sahara one": "Entertainment",
    "dangal": "Entertainment",
    "dangal 2": "Entertainment",
    "big magic": "Entertainment",
    "shemaaroo tv": "Entertainment",
    "shemaroo tv": "Entertainment",
    "dd national": "Entertainment",
    "dd national hd": "Entertainment",
    "dd kisan": "Infotainment",
    "dd bharati": "Entertainment",
    "dd india": "News",
    "dd urdu": "Entertainment",

    # ---------------- MOVIES ----------------
    "zee cinema": "Movies",
    "zee cinema hd": "Movies",
    "sony max": "Movies",
    "sony max 2": "Movies",
    "sony wah": "Movies",
    "star gold": "Movies",
    "star gold hd": "Movies",
    "star gold select": "Movies",
    "star gold select hd": "Movies",
    "star gold 2": "Movies",
    "b4u movies": "Movies",
    "b4u movies hd": "Movies",
    "bollywood 4u": "Movies",
    "bollywood 4u hd": "Movies",
    "shemaroo bollywood": "Movies",
    "shemaroo bollywood hd": "Movies",
    "shemaroo me": "Movies",
    "filmy": "Movies",
    "wow cinema": "Movies",
    "mastiii": "Movies",
    "manoranjan tv": "Movies",
    "manoranjan grand": "Movies",
    "movie plus": "Movies",
    "goldmines": "Movies",
    "goldmines bollywood": "Movies",
    "goldmines movies": "Movies",
    "raj digital plus": "Movies",
    "raj tv": "Movies",

    # ---------------- MUSIC ----------------
    "mtv": "Music",
    "mtv beats": "Music",
    "9xm": "Music",
    "9x music": "Music",
    "9x jhakaas": "Music",
    "music india": "Music",
    "b4u music": "Music",
    "zoom": "Music",
    "mastiii": "Music",
    "e24": "Music",
    "9x tashan": "Music",
    "9x jalwa": "Music",
    "dhoom music": "Music",

    # ---------------- KIDS ----------------
    "cartoon network": "Kids",
    "cartoon network hd": "Kids",
    "pogo": "Kids",
    "discovery kids": "Kids",
    "nick": "Kids",
    "nick hd+": "Kids",
    "nickelodeon": "Kids",
    "sonic": "Kids",
    "hungama": "Kids",
    "hungama tv": "Kids",
    "super hungama": "Kids",
    "disney channel": "Kids",
    "disney junior": "Kids",
    "disney xd": "Kids",

    # ---------------- SCIENCE ----------------
    "discovery science": "Science",
    "discovery science hd": "Science",
    "nat geo": "Science",
    "natgeo": "Science",
    "national geographic": "Science",
    "national geographic hd": "Science",
    "history tv18": "Science",
    "history tv18 hd": "Science",
    "history": "Science",
    "animal planet": "Science",
    "animal planet hd": "Science",
    "nasa tv": "Science",

    # ---------------- INFOTAINMENT ----------------
    "discovery": "Infotainment",
    "discovery hd": "Infotainment",
    "discovery channel": "Infotainment",
    "discovery turbo": "Infotainment",
    "discovery world": "Infotainment",
    "discovery hd world": "Infotainment",
    "tlc": "Infotainment",
    "tlc hd": "Infotainment",
    "travelxp": "Lifestyle",
    "travelxp hd": "Lifestyle",
    "food food": "Lifestyle",
    "epic": "Infotainment",
    "epic tv": "Infotainment",
    "sony bbc earth": "Science",
    "sony bbc earth hd": "Science",
    "good times": "Lifestyle",
    "fashion tv": "Lifestyle",
    "ftv": "Lifestyle",

    # ---------------- SPORTS ----------------
    "star sports": "Sports",
    "star sports 1": "Sports",
    "star sports 1 hd": "Sports",
    "star sports 2": "Sports",
    "star sports 2 hd": "Sports",
    "star sports 3": "Sports",
    "star sports 3 hd": "Sports",
    "star sports 1 hindi": "Sports",
    "star sports hindi": "Sports",
    "star sports select 1": "Sports",
    "star sports select 1 hd": "Sports",
    "star sports select 2": "Sports",
    "star sports select 2 hd": "Sports",
    "star sports first": "Sports",
    "sony sports ten 1": "Sports",
    "sony sports ten 2": "Sports",
    "sony sports ten 3": "Sports",
    "sony ten 1": "Sports",
    "sony ten 2": "Sports",
    "sony ten 3": "Sports",
    "sony ten 4": "Sports",
    "sony ten 5": "Sports",
    "sony sports": "Sports",
    "eurosport": "Sports",
    "eurosport hd": "Sports",
    "dd sports": "Sports",
    "sports18": "Sports",
    "sports18 1": "Sports",
    "sports18 2": "Sports",
    "sports18 khel": "Sports",
    "jio sports": "Sports",
    "jio sports 1": "Sports",
    "jio sports 2": "Sports",
    "jio cricket": "Sports",
    "jio football": "Sports",
    "willow": "Sports",
    "willow cricket": "Sports",
    "ten cricket": "Sports",
    "fox cricket": "Sports",
}

# Channels where keyword matching is safe.
KEYWORD_GROUPS = [
    (("news", "samachar"), "News"),
    (("business", "cnbc", "bloomberg", "et now"), "Business"),
    (("cricket", "sports", "sport", "football", "hockey", "tennis"), "Sports"),
    (("cartoon", "kids", "nick", "pogo", "hungama", "sonic", "disney"), "Kids"),
    (("movie", "cinema", "bollywood", "filmy", "goldmines"), "Movies"),
    (("music", "beats", "9xm", "zoom"), "Music"),
    (("science", "discovery science", "nat geo", "national geographic"), "Science"),
    (("travel", "food food", "fashion"), "Lifestyle"),
    (("discovery", "history", "animal planet", "tlc", "epic"), "Infotainment"),
]

# Foreign cricket is explicitly allowed.
FOREIGN_CRICKET_WORDS = (
    "cricket", "willow", "fox cricket", "ten cricket",
    "sky sports cricket", "supersport cricket"
)

# Generic names are too dangerous for fuzzy matching.
GENERIC_NAMES = {
    "news",
    "music",
    "movies",
    "sports",
    "entertainment",
    "live",
    "channel",
    "tv",
    "india",
}

# ============================================================
# HELPERS
# ============================================================

def norm(value):
    value = value or ""
    value = value.lower()
    value = value.replace("&", "and")
    value = re.sub(r"[|:_\-./]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def clean_name(name):
    name = name or ""
    name = re.sub(r"\s*\[[^\]]+\]\s*", " ", name)
    name = re.sub(r"\s*\([^)]+\)\s*", " ", name)
    name = re.sub(
        r"\b(hd|fhd|uhd|4k|sd|hevc|h265|h264|1080p|720p|576p|480p)\b",
        "",
        name,
        flags=re.I,
    )
    name = re.sub(r"\s+", " ", name)
    return name.strip(" -|")


def parse_attrs(line):
    attrs = {}

    for key, value in re.findall(r'([\w-]+)="([^"]*)"', line):
        attrs[key.lower()] = value

    return attrs


def get_language(info, name, source_name):
    attrs = parse_attrs(info)

    candidates = [
        attrs.get("tvg-language", ""),
        attrs.get("language", ""),
        attrs.get("group-title", ""),
        name,
        source_name,
    ]

    text = " ".join(candidates).lower()

    # Explicit language has highest priority.
    if re.search(r"\bbhojpuri\b", text):
        return "Bhojpuri"

    if re.search(r"\bhindi\b", text):
        return "Hindi"

    if re.search(r"\benglish\b", text):
        return "English"

    # Source playlist itself is a language hint.
    source = source_name.lower()

    if "playlist-hindi" in source:
        return "Hindi"

    if "playlist-english-india" in source:
        return "English"

    # If an unwanted regional language is explicitly present,
    # reject it instead of guessing.
    for lang in OTHER_REGIONAL_LANGUAGES:
        if re.search(r"\b" + re.escape(lang) + r"\b", text):
            return None

    return None


def is_foreign_cricket(name, info):
    text = norm(name + " " + info)
    return any(word in text for word in FOREIGN_CRICKET_WORDS)


def exact_channel_group(name):
    n = norm(clean_name(name))

    if not n or n in GENERIC_NAMES:
        return None

    # Exact first.
    for channel, group in CHANNEL_GROUPS.items():
        if n == norm(channel):
            return group

    return None


def classify_channel(name, info):
    """
    Source group-title is deliberately ignored.

    Classification follows known JioTV-style channel names,
    then conservative channel-name keywords.
    """

    exact = exact_channel_group(name)
    if exact:
        return exact

    n = norm(clean_name(name))

    # Sports first so e.g. "Star Sports Cricket" never becomes
    # Entertainment/Infotainment.
    for words, group in KEYWORD_GROUPS:
        for word in words:
            if word in n:
                return group

    return None


def is_allowed_language(language):
    if not language:
        return False
    return language.lower() in ALLOWED_LANGUAGES


def canonical_url(url):
    """
    Exact URL deduplication.

    Do not alter query parameters because different parameters
    may represent different streams.
    """
    return url.strip()


def parse_m3u(text, source_name):
    entries = []

    lines = text.splitlines()
    current_info = None
    current_name = None

    for raw in lines:
        line = raw.strip()

        if not line:
            continue

        if line.startswith("#EXTINF"):
            current_info = line
            current_name = line.split(",", 1)[1].strip() if "," in line else ""
            continue

        if line.startswith("#"):
            continue

        if current_info is None:
            continue

        url = line.strip()

        if not url:
            continue

        entries.append({
            "info": current_info,
            "name": current_name or "",
            "url": url,
            "source": source_name,
        })

        current_info = None
        current_name = None

    return entries


def download(url):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 IPTV-Playlist-Generator",
            "Accept": "*/*",
        },
    )

    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read().decode("utf-8", errors="replace")


def rebuild_extinf(entry, group, language):
    attrs = parse_attrs(entry["info"])

    # Remove old group/language so the generated playlist has
    # only our own metadata.
    attrs["group-title"] = group
    attrs["tvg-language"] = language

    # Preserve useful existing attributes.
    ordered = []

    preferred = [
        "tvg-id",
        "tvg-name",
        "tvg-logo",
        "tvg-language",
        "group-title",
    ]

    used = set()

    for key in preferred:
        if key in attrs:
            ordered.append(f'{key}="{attrs[key]}"')
            used.add(key)

    for key, value in attrs.items():
        if key not in used:
            ordered.append(f'{key}="{value}"')

    return "#EXTINF:-1 " + " ".join(ordered) + "," + entry["name"]


# ============================================================
# MAIN
# ============================================================

def main():
    output = "playlist.m3u"

    if "-o" in sys.argv:
        try:
            output = sys.argv[sys.argv.index("-o") + 1]
        except IndexError:
            pass

    print("==============================================")
    print(" JioTV-style Indian Channel Playlist Builder")
    print("==============================================")
    print("Sources:", len(SOURCE_URLS))

    all_entries = []

    for source_url in SOURCE_URLS:
        source_name = Path(urlsplit(source_url).path).name

        print(f"\nFetching: {source_name}")

        try:
            text = download(source_url)
            entries = parse_m3u(text, source_name)

            print(f"  Entries: {len(entries)}")
            all_entries.extend(entries)

        except Exception as exc:
            print(f"  ERROR: {exc}")

    print(f"\nTotal source entries: {len(all_entries)}")

    final = []

    # Exact URL is globally unique.
    # This automatically removes:
    #   same channel + same URL
    #   different channel + same URL
    seen_urls = set()

    rejected_language = 0
    rejected_group = 0
    rejected_foreign = 0

    for entry in all_entries:
        name = clean_name(entry["name"])
        info = entry["info"]
        url = canonical_url(entry["url"])

        if not url:
            continue

        # ----------------------------------------------------
        # LANGUAGE
        # ----------------------------------------------------
        language = get_language(
            info,
            name,
            entry["source"],
        )

        # Foreign cricket is the one explicit foreign exception.
        foreign_cricket = is_foreign_cricket(name, info)

        if not foreign_cricket:
            if not is_allowed_language(language):
                rejected_language += 1
                continue
        else:
            # Keep cricket even if the playlist doesn't explicitly
            # mark it as Hindi/English/Bhojpuri.
            if not language:
                language = "English"

        # ----------------------------------------------------
        # GROUP
        # ----------------------------------------------------
        group = classify_channel(name, info)

        # Foreign cricket always belongs to Sports.
        if foreign_cricket:
            group = "Sports"

        if group not in ALLOWED_GROUPS:
            rejected_group += 1
            continue

        # ----------------------------------------------------
        # GLOBAL EXACT URL DEDUP
        # ----------------------------------------------------
        if url in seen_urls:
            continue

        seen_urls.add(url)

        final.append({
            "entry": entry,
            "name": name,
            "url": url,
            "group": group,
            "language": language,
        })

    # --------------------------------------------------------
    # Stable ordering:
    # exact 10 groups only
    # --------------------------------------------------------
    group_order = {
        group: index
        for index, group in enumerate(ALLOWED_GROUPS)
    }

    final.sort(
        key=lambda x: (
            group_order.get(x["group"], 999),
            norm(x["name"]),
            x["url"],
        )
    )

    # --------------------------------------------------------
    # WRITE PLAYLIST
    # --------------------------------------------------------
    with open(output, "w", encoding="utf-8", newline="\n") as fp:
        fp.write("#EXTM3U\n")

        current_group = None

        for item in final:
            if item["group"] != current_group:
                current_group = item["group"]
                fp.write(
                    f'\n# ===== {current_group} =====\n'
                )

            fp.write(
                rebuild_extinf(
                    item["entry"],
                    item["group"],
                    item["language"],
                )
                + "\n"
            )

            fp.write(item["url"] + "\n")

    # --------------------------------------------------------
    # STATS
    # --------------------------------------------------------
    counts = {group: 0 for group in ALLOWED_GROUPS}

    for item in final:
        counts[item["group"]] += 1

    print("\n==============================================")
    print(" FINAL PLAYLIST")
    print("==============================================")

    for group in ALLOWED_GROUPS:
        print(f"{group:15} : {counts[group]}")

    print("----------------------------------------------")
    print("Source entries       :", len(all_entries))
    print("Final unique URLs    :", len(final))
    print("Rejected language    :", rejected_language)
    print("Rejected category    :", rejected_group)
    print("Output               :", output)
    print("==============================================")


if __name__ == "__main__":
    main()
