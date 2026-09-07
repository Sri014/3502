#!/usr/bin/env python3

import re
import urllib.request
from pathlib import Path


# ============================================================
# SOURCES
# ============================================================

SOURCE_URLS = [

    # ---------------- INDIA / HINDI ----------------
    "https://iptv-org.github.io/iptv/languages/hin.m3u",

    # ---------------- BHOJPURI ----------------
    "https://iptv-org.github.io/iptv/languages/bho.m3u",

    # ---------------- ENGLISH ----------------
    "https://iptv-org.github.io/iptv/languages/eng.m3u",

    # ---------------- SPORTS ----------------
    "https://iptv-org.github.io/iptv/categories/sports.m3u",

    # ---------------- KIDS ----------------
    "https://iptv-org.github.io/iptv/categories/kids.m3u",

    # ---------------- ENTERTAINMENT ----------------
    "https://iptv-org.github.io/iptv/categories/entertainment.m3u",

    # ---------------- SCIENCE ----------------
    "https://iptv-org.github.io/iptv/categories/science.m3u",

    # ---------------- LIFESTYLE ----------------
    "https://iptv-org.github.io/iptv/categories/lifestyle.m3u",

    # ========================================================
    # FOREIGN HINDI FEEDS
    # UK
    # ========================================================

    "https://iptv-org.github.io/iptv/countries/uk.m3u",

    # USA
    "https://iptv-org.github.io/iptv/countries/us.m3u",

    # CANADA
    "https://iptv-org.github.io/iptv/countries/ca.m3u",

    # Middle East
    "https://iptv-org.github.io/iptv/countries/ae.m3u",
    "https://iptv-org.github.io/iptv/countries/qa.m3u",
    "https://iptv-org.github.io/iptv/countries/sa.m3u",

    # ========================================================
    # DISABLED
    # ========================================================

    # TV Garden webpage is NOT an M3U:
    # "https://tvgarden.world/tv/in",

    # Wizakor disabled:
    # "https://raw.githubusercontent.com/wizakorhd/iptv/main/playlist-hindi.m3u",
    # "https://raw.githubusercontent.com/wizakorhd/iptv/refs/heads/main/playlist-top.m3u",
    # "https://raw.githubusercontent.com/wizakorhd/iptv/refs/heads/main/playlist-english-india.m3u",
]


# ============================================================
# FINAL GROUPS
# ============================================================

GROUPS = [
    "Hindi",
    "English",
    "Bhojpuri",
    "Sports - Cricket",
    "Sports - Hockey",
    "Sports - Football",
    "Sports - WWE",
    "Sports - Tennis",
    "Sports",
    "Kids",
    "Entertainment",
    "Information",
    "Science",
    "Lifestyle",
    "Radio",
]


# ============================================================
# USER AGENT
# ============================================================

USER_AGENT = (
    "Mozilla/5.0 "
    "(Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/140.0 Safari/537.36"
)


# ============================================================
# FETCH
# ============================================================

def fetch_text(url):

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "*/*",
        },
    )

    with urllib.request.urlopen(
        request,
        timeout=60,
    ) as response:

        data = response.read()

    for encoding in (
        "utf-8-sig",
        "utf-8",
        "latin-1",
    ):

        try:
            return data.decode(encoding)

        except UnicodeDecodeError:
            pass

    return data.decode(
        "utf-8",
        errors="replace"
    )


# ============================================================
# CLEAN
# ============================================================

def clean_text(value):

    if value is None:
        return ""

    value = str(value)

    replacements = {
        "&amp;": "&",
        "&quot;": '"',
        "&#39;": "'",
        "&apos;": "'",
    }

    for old, new in replacements.items():
        value = value.replace(old, new)

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


def normalize_text(value):

    value = clean_text(value).lower()

    value = value.replace(
        "&",
        " and "
    )

    value = re.sub(
        r"[^a-z0-9]+",
        " ",
        value
    )

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


# ============================================================
# ATTRIBUTES
# ============================================================

def parse_attrs(line):

    attrs = {}

    for match in re.finditer(
        r'([\w-]+)="([^"]*)"',
        line
    ):

        attrs[
            match.group(1)
        ] = match.group(2)

    return attrs


# ============================================================
# M3U PARSER
# ============================================================

def parse_m3u(text):

    entries = []

    current = None

    pending_options = []

    for raw in text.splitlines():

        line = raw.strip()

        if not line:
            continue

        if line.startswith(
            "#EXTVLCOPT:"
        ):

            if current is not None:

                current.setdefault(
                    "options",
                    []
                ).append(line)

            else:

                pending_options.append(
                    line
                )

            continue

        if line.startswith(
            "#EXTINF:"
        ):

            current = {
                "extinf": line,
                "name": "",
                "url": "",
                "attrs": parse_attrs(line),
                "options": list(
                    pending_options
                ),
            }

            pending_options = []

            comma = line.find(",")

            if comma >= 0:

                current["name"] = clean_text(
                    line[comma + 1:]
                )

            continue

        if (
            current is not None
            and not line.startswith("#")
        ):

            current["url"] = clean_text(
                line
            )

            if current["url"]:

                entries.append(
                    current
                )

            current = None

    return entries


# ============================================================
# ATTR
# ============================================================

def get_attr(entry, *names):

    attrs = entry.get(
        "attrs",
        {}
    )

    for name in names:

        value = attrs.get(name)

        if value:
            return clean_text(value)

    return ""


def channel_name(entry):

    return (
        clean_text(
            entry.get(
                "name",
                ""
            )
        )
        or get_attr(
            entry,
            "tvg-name",
            "channel-name",
            "name"
        )
        or "Unknown"
    )


def channel_group(entry):

    return get_attr(
        entry,
        "group-title"
    )


# ============================================================
# EXCLUDE UNWANTED CHANNELS
# ============================================================

REMOVE_WORDS = (

    # Educational channels requested to remove
    "swayam prabha",
    "swayamprabha",
    "pm e vidya",
    "pm e-vidya",
    "pmevidya",
    "pm evidya",
    "vande gujarat",
    "vande gujrat",

)


def is_removed(entry):

    text = normalize_text(
        channel_name(entry)
        + " "
        + channel_group(entry)
    )

    for word in REMOVE_WORDS:

        if normalize_text(word) in text:

            return True

    return False


# ============================================================
# SPORTS GROUPING
# ============================================================

def sports_group(name, group):

    text = normalize_text(
        name + " " + group
    )

    # Cricket
    if any(word in text for word in (
        "cricket",
        "willow",
        "fox cricket",
        "sky cricket",
        "super sport cricket",
        "supersport cricket",
        "ten cricket",
        "sony sports ten 3",
        "sony ten 3",
        "star sports cricket",
        "icc",
    )):

        return "Sports - Cricket"


    # Hockey
    if any(word in text for word in (
        "hockey",
        "nhl",
        "field hockey",
        "ice hockey",
    )):

        return "Sports - Hockey"


    # Football
    if any(word in text for word in (
        "football",
        "soccer",
        "sky sports football",
        "tnt sports football",
        "premier league",
        "epl",
        "uefa",
        "champions league",
        "fifa",
    )):

        return "Sports - Football"


    # WWE
    if any(word in text for word in (
        "wwe",
        "world wrestling",
        "wrestling",
        "raw",
        "smackdown",
    )):

        return "Sports - WWE"


    # Tennis
    if any(word in text for word in (
        "tennis",
        "atp",
        "wta",
        "us open",
        "french open",
        "wimbledon",
        "australian open",
    )):

        return "Sports - Tennis"


    return "Sports"


# ============================================================
# CHANNEL GROUPING
# ============================================================

def group_channel(entry):

    name = normalize_text(
        channel_name(entry)
    )

    original = normalize_text(
        channel_group(entry)
    )

    combined = name + " " + original


    # --------------------------------------------------------
    # REMOVE UNWANTED
    # --------------------------------------------------------

    if is_removed(entry):

        return None


    # --------------------------------------------------------
    # SPORTS
    # --------------------------------------------------------

    if any(word in combined for word in (
        "sport",
        "cricket",
        "hockey",
        "football",
        "soccer",
        "wwe",
        "tennis",
        "willow",
        "supersport",
        "sky sports",
        "tnt sports",
        "fox sports",
        "espn",
        "bein sports",
        "eurosport",
    )):

        return sports_group(
            name,
            original
        )


    # --------------------------------------------------------
    # BHOJPURI
    # --------------------------------------------------------

    if any(word in combined for word in (
        "bhojpuri",
        "bhojpuriya",
    )):

        return "Bhojpuri"


    # --------------------------------------------------------
    # HINDI
    # --------------------------------------------------------

    if any(word in combined for word in (
        "hindi",
        "aaj tak",
        "zee news",
        "zee tv",
        "sony sab",
        "sony pal",
        "sony entertainment",
        "utsav",
        "star plus",
        "colors",
        "dangal",
        "and tv",
        "dd national",
        "dd india",
        "zee cinema",
        "sony max",
    )):

        return "Hindi"


    # --------------------------------------------------------
    # ENGLISH
    # --------------------------------------------------------

    if "english" in combined:

        return "English"


    # --------------------------------------------------------
    # KIDS
    # --------------------------------------------------------

    if any(word in combined for word in (
        "kids",
        "kid",
        "cartoon",
        "nick",
        "nickelodeon",
        "disney",
        "pogo",
        "sonic",
        "baby",
        "junior",
        "anime",
    )):

        return "Kids"


    # --------------------------------------------------------
    # SCIENCE
    # --------------------------------------------------------

    if any(word in combined for word in (
        "science",
        "discovery science",
        "national geographic",
        "nat geo",
        "animal planet",
        "history",
        "discovery",
        "documentary",
        "technology",
        "knowledge",
    )):

        return "Science"


    # --------------------------------------------------------
    # LIFESTYLE
    # --------------------------------------------------------

    if any(word in combined for word in (
        "lifestyle",
        "fashion",
        "food",
        "travel",
        "living",
        "home",
        "cooking",
    )):

        return "Lifestyle"


    # --------------------------------------------------------
    # INFORMATION
    # --------------------------------------------------------

    if any(word in combined for word in (
        "news",
        "information",
        "informational",
        "business",
        "cnbc",
        "bloomberg",
        "finance",
        "financial",
        "money",
        "market",
        "india today",
        "times now",
        "republic",
        "tv9",
        "wion",
    )):

        return "Information"


    # --------------------------------------------------------
    # ENTERTAINMENT
    # --------------------------------------------------------

    if any(word in combined for word in (
        "entertainment",
        "movie",
        "movies",
        "cinema",
        "film",
        "bollywood",
        "hollywood",
        "sony",
        "zee",
        "colors",
        "star",
        "sab",
        "dangal",
    )):

        return "Entertainment"


    # --------------------------------------------------------
    # DEFAULT
    # --------------------------------------------------------

    return "Entertainment"


# ============================================================
# EXTINF
# ============================================================

def escape_m3u(value):

    return clean_text(
        value
    ).replace(
        '"',
        "'"
    )


def build_extinf(entry, group):

    attrs = entry.get(
        "attrs",
        {}
    )

    name = channel_name(entry)

    output_attrs = []

    preferred = [
        "tvg-id",
        "tvg-chno",
        "tvg-logo",
        "resolution",
        "subs",
    ]

    for key in preferred:

        value = attrs.get(key)

        if value:

            output_attrs.append(
                f'{key}="{escape_m3u(value)}"'
            )

    output_attrs.append(
        f'group-title="{group}"'
    )

    already = set(
        preferred
        + ["group-title"]
    )

    for key, value in attrs.items():

        if key in already:
            continue

        if not value:
            continue

        output_attrs.append(
            f'{key}="{escape_m3u(value)}"'
        )

    return (
        "#EXTINF:-1 "
        + " ".join(output_attrs)
        + ","
        + escape_m3u(name)
    )


# ============================================================
# LOAD
# ============================================================

def load_sources():

    all_entries = []

    print()
    print("========================================")
    print("FETCHING VERIFIED IPTV SOURCES")
    print("========================================")

    for url in SOURCE_URLS:

        filename = url.rsplit(
            "/",
            1
        )[-1]

        try:

            text = fetch_text(url)

            entries = parse_m3u(
                text
            )

            print(
                f"{filename:35} "
                f"{len(entries):5} channels"
            )

            all_entries.extend(
                entries
            )

        except Exception as exc:

            print(
                f"{filename:35} FAILED"
            )

            print(
                f"  {type(exc).__name__}: {exc}"
            )

    return all_entries


# ============================================================
# MAIN
# ============================================================

def main():

    output_file = Path(
        "playlist.m3u"
    )

    entries = load_sources()

    print()
    print("========================================")
    print("SOURCE RESULT")
    print("========================================")

    print(
        f"Total entries : {len(entries)}"
    )


    # --------------------------------------------------------
    # URL DEDUP
    # --------------------------------------------------------

    seen_urls = set()

    unique_entries = []

    duplicate_count = 0

    for entry in entries:

        url = clean_text(
            entry.get(
                "url",
                ""
            )
        )

        if not url:
            continue

        key = url.lower().strip()

        if key in seen_urls:

            duplicate_count += 1

            continue

        seen_urls.add(key)

        unique_entries.append(
            entry
        )


    print(
        f"Unique URLs   : "
        f"{len(unique_entries)}"
    )

    print(
        f"Duplicates    : "
        f"{duplicate_count}"
    )


    # --------------------------------------------------------
    # GROUP
    # --------------------------------------------------------

    grouped = {
        group: []
        for group in GROUPS
    }

    removed = 0

    for entry in unique_entries:

        group = group_channel(
            entry
        )

        if group is None:

            removed += 1

            continue

        if group not in grouped:

            group = "Entertainment"

        grouped[group].append(
            entry
        )


    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    for group in GROUPS:

        grouped[group].sort(
            key=lambda entry: (
                normalize_text(
                    channel_name(entry)
                ),
                clean_text(
                    entry.get(
                        "url",
                        ""
                    )
                ).lower(),
            )
        )


    # --------------------------------------------------------
    # BUILD PLAYLIST
    # --------------------------------------------------------

    lines = [
        "#EXTM3U"
    ]

    total = 0

    for group in GROUPS:

        for entry in grouped[group]:

            lines.append(
                build_extinf(
                    entry,
                    group
                )
            )

            for option in entry.get(
                "options",
                []
            ):

                lines.append(option)

            lines.append(
                clean_text(
                    entry["url"]
                )
            )

            total += 1


    # --------------------------------------------------------
    # WRITE
    # --------------------------------------------------------

    output_file.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    print()
    print("========================================")
    print("PLAYLIST COMPLETE")
    print("========================================")

    print(
        f"Final streams : {total}"
    )

    print(
        f"Removed       : {removed}"
    )

    print(
        f"Output        : {output_file}"
    )

    print()

    for group in GROUPS:

        print(
            f"{group:22} : "
            f"{len(grouped[group])}"
        )


if __name__ == "__main__":

    main()
