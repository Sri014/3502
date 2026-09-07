#!/usr/bin/env python3

import re
import urllib.request
from pathlib import Path


# ============================================================
# SOURCE PLAYLISTS
# ============================================================

SOURCE_URLS = [
    "https://raw.githubusercontent.com/wizakorhd/iptv/main/playlist-hindi.m3u",
    "https://raw.githubusercontent.com/wizakorhd/iptv/refs/heads/main/playlist-top.m3u",
    "https://raw.githubusercontent.com/wizakorhd/iptv/refs/heads/main/playlist-english-india.m3u",
]


# ============================================================
# FINAL GROUP ORDER
# ============================================================

GROUPS = [
    "News",
    "Entertainment",
    "Movies",
    "Music",
    "Kids",
    "Infotainment",
    "Business",
    "Lifestyle",
    "Sports",
]


# ============================================================
# HTTP
# ============================================================

USER_AGENT = (
    "Mozilla/5.0 "
    "(Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/140.0 Safari/537.36"
)


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
        errors="replace",
    )


# ============================================================
# TEXT
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
        value = value.replace(
            old,
            new,
        )

    value = re.sub(
        r"\s+",
        " ",
        value,
    )

    return value.strip()


def normalize_text(value):
    value = clean_text(
        value
    ).lower()

    value = value.replace(
        "&",
        " and ",
    )

    value = re.sub(
        r"[^a-z0-9]+",
        " ",
        value,
    )

    value = re.sub(
        r"\s+",
        " ",
        value,
    )

    return value.strip()


# ============================================================
# M3U ATTRIBUTE PARSER
# ============================================================

def parse_attrs(line):
    attrs = {}

    for match in re.finditer(
        r'([\w-]+)="([^"]*)"',
        line,
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

        # ----------------------------------------------------
        # VLC OPTIONS
        # ----------------------------------------------------

        if line.startswith(
            "#EXTVLCOPT:"
        ):
            if current is not None:
                current.setdefault(
                    "options",
                    [],
                ).append(line)
            else:
                pending_options.append(
                    line
                )

            continue

        # ----------------------------------------------------
        # EXTINF
        # ----------------------------------------------------

        if line.startswith(
            "#EXTINF:"
        ):

            current = {
                "extinf": line,
                "name": "",
                "url": "",
                "attrs": parse_attrs(
                    line
                ),
                "options": list(
                    pending_options
                ),
            }

            pending_options = []

            comma = line.find(",")

            if comma >= 0:
                current["name"] = clean_text(
                    line[
                        comma + 1:
                    ]
                )

            continue

        # ----------------------------------------------------
        # URL
        # ----------------------------------------------------

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
# ATTRIBUTES
# ============================================================

def get_attr(
    entry,
    *names,
):
    attrs = entry.get(
        "attrs",
        {},
    )

    for name in names:

        value = attrs.get(
            name
        )

        if value:
            return clean_text(
                value
            )

    return ""


def channel_name(entry):
    return (
        clean_text(
            entry.get(
                "name",
                "",
            )
        )
        or get_attr(
            entry,
            "tvg-name",
            "channel-name",
            "name",
        )
        or "Unknown"
    )


def channel_group(entry):
    return get_attr(
        entry,
        "group-title",
    )


# ============================================================
# GROUPING
# ============================================================

def group_channel(
    entry
):
    """
    Convert Wizakor group-title into the
    requested clean groups.

    IMPORTANT:
    No channel is rejected here.
    """

    original = channel_group(
        entry
    )

    value = normalize_text(
        original
    )

    name = normalize_text(
        channel_name(entry)
    )

    # --------------------------------------------------------
    # SPORTS
    # --------------------------------------------------------

    sports_words = (
        "sport",
        "sports",
        "cricket",
        "willow",
        "sky sports",
        "ten sports",
        "star sports",
        "sony sports",
        "espn",
        "eurosport",
        "bein sports",
        "fox sports",
        "icc",
        "football",
        "fifa",
        "tennis",
        "golf",
        "nba",
        "nfl",
        "nhl",
        "mlb",
    )

    if any(
        word in name
        for word in sports_words
    ):
        return "Sports"

    if (
        "sport" in value
        or "sports" in value
    ):
        return "Sports"

    # --------------------------------------------------------
    # NEWS
    # --------------------------------------------------------

    news_words = (
        "news",
        "aaj tak",
        "ndtv",
        "cnn",
        "bbc news",
        "republic",
        "times now",
        "india today",
        "news18",
        "zee news",
        "abp news",
        "tv9",
        "wion",
        "cnbc",
        "business today",
    )

    if any(
        word in name
        for word in news_words
    ):
        return "News"

    if "news" in value:
        return "News"

    # --------------------------------------------------------
    # MOVIES
    # --------------------------------------------------------

    movie_words = (
        "movie",
        "movies",
        "film",
        "films",
        "cinema",
        "bollywood",
        "hollywood",
        "action",
        "pictures",
        "flix",
        "colors cineplex",
        "zee cinema",
        "sony max",
        "star gold",
        "and pictures",
        "shemaroo",
    )

    if any(
        word in name
        for word in movie_words
    ):
        return "Movies"

    if any(
        word in value
        for word in (
            "movie",
            "movies",
            "film",
            "cinema",
        )
    ):
        return "Movies"

    # --------------------------------------------------------
    # MUSIC
    # --------------------------------------------------------

    music_words = (
        "music",
        "mtv",
        "9xm",
        "9x music",
        "b4u music",
        "zoom",
        "mastiii",
        "hungama music",
        "songs",
    )

    if any(
        word in name
        for word in music_words
    ):
        return "Music"

    if "music" in value:
        return "Music"

    # --------------------------------------------------------
    # KIDS
    # --------------------------------------------------------

    kids_words = (
        "kids",
        "cartoon",
        "nick",
        "nickelodeon",
        "disney",
        "pogo",
        "hungama",
        "sonic",
        "baby",
        "junior",
        "anime",
    )

    if any(
        word in name
        for word in kids_words
    ):
        return "Kids"

    if (
        "kid" in value
        or "children" in value
        or "anime" in value
    ):
        return "Kids"

    # --------------------------------------------------------
    # BUSINESS
    # --------------------------------------------------------

    business_words = (
        "business",
        "cnbc",
        "bloomberg",
        "money",
        "market",
        "financial",
    )

    if any(
        word in name
        for word in business_words
    ):
        return "Business"

    if "business" in value:
        return "Business"

    # --------------------------------------------------------
    # LIFESTYLE
    # --------------------------------------------------------

    lifestyle_words = (
        "lifestyle",
        "fashion",
        "food",
        "travel",
        "living",
        "home",
        "cook",
        "cooking",
    )

    if any(
        word in name
        for word in lifestyle_words
    ):
        return "Lifestyle"

    if any(
        word in value
        for word in (
            "lifestyle",
            "fashion",
            "food",
            "travel",
        )
    ):
        return "Lifestyle"

    # --------------------------------------------------------
    # INFOTAINMENT
    # --------------------------------------------------------

    infotainment_words = (
        "discovery",
        "history",
        "national geographic",
        "nat geo",
        "animal planet",
        "documentary",
        "science",
        "technology",
        "knowledge",
        "infotainment",
        "wild",
        "explore",
    )

    if any(
        word in name
        for word in infotainment_words
    ):
        return "Infotainment"

    if any(
        word in value
        for word in (
            "infotainment",
            "documentary",
            "science",
            "technology",
            "travel",
        )
    ):
        return "Infotainment"

    # --------------------------------------------------------
    # ENTERTAINMENT
    # --------------------------------------------------------

    entertainment_words = (
        "entertainment",
        "ent",
        "colors",
        "zee tv",
        "sony",
        "star plus",
        "star bharat",
        "sab",
        "dangal",
        "and tv",
        "dd national",
        "dd india",
        "sun tv",
        "general entertainment",
    )

    if any(
        word in name
        for word in entertainment_words
    ):
        return "Entertainment"

    if (
        "entertainment" in value
        or "general" in value
    ):
        return "Entertainment"

    # --------------------------------------------------------
    # ORIGINAL GROUP FALLBACK
    # --------------------------------------------------------

    if "news" in value:
        return "News"

    if "movie" in value:
        return "Movies"

    if "music" in value:
        return "Music"

    if "kid" in value:
        return "Kids"

    if "sport" in value:
        return "Sports"

    if "business" in value:
        return "Business"

    if "lifestyle" in value:
        return "Lifestyle"

    if "infotainment" in value:
        return "Infotainment"

    # --------------------------------------------------------
    # UNKNOWN
    #
    # Do NOT drop it.
    # Entertainment is safer than losing a channel.
    # --------------------------------------------------------

    return "Entertainment"


# ============================================================
# URL NORMALIZATION
# ============================================================

def url_key(url):
    """
    Exact URL dedup.

    Same URL appearing in two source playlists
    will be kept only once.
    """

    return clean_text(
        url
    ).strip().lower()


# ============================================================
# ESCAPE
# ============================================================

def escape_m3u(value):
    return clean_text(
        value
    ).replace(
        '"',
        "'",
    )


# ============================================================
# BUILD EXTINF
# ============================================================

def build_extinf(
    entry,
    group,
):
    attrs = entry.get(
        "attrs",
        {},
    )

    name = channel_name(
        entry
    )

    # --------------------------------------------------------
    # Preserve original attributes
    # --------------------------------------------------------

    output_attrs = []

    preferred = [
        "tvg-id",
        "tvg-chno",
        "tvg-logo",
        "resolution",
        "subs",
    ]

    for key in preferred:

        value = attrs.get(
            key
        )

        if value:
            output_attrs.append(
                f'{key}="{escape_m3u(value)}"'
            )

    # --------------------------------------------------------
    # Our clean group
    # --------------------------------------------------------

    output_attrs.append(
        f'group-title="{group}"'
    )

    # --------------------------------------------------------
    # Preserve other useful attributes
    # --------------------------------------------------------

    already = set(
        preferred
        + [
            "group-title",
        ]
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
        + " ".join(
            output_attrs
        )
        + ","
        + escape_m3u(name)
    )


# ============================================================
# LOAD ALL THREE PLAYLISTS
# ============================================================

def load_sources():

    all_entries = []

    print()
    print(
        "========================================"
    )
    print(
        "FETCHING WIZAKOR PLAYLISTS"
    )
    print(
        "========================================"
    )

    for url in SOURCE_URLS:

        filename = url.rsplit(
            "/",
            1,
        )[-1]

        try:

            text = fetch_text(
                url
            )

            entries = parse_m3u(
                text
            )

            print(
                f"{filename:30} "
                f"{len(entries):4} channels"
            )

            all_entries.extend(
                entries
            )

        except Exception as exc:

            print(
                f"{filename:30} FAILED"
            )

            print(
                f"  {type(exc).__name__}: "
                f"{exc}"
            )

    return all_entries


# ============================================================
# MAIN
# ============================================================

def main():

    output_file = Path(
        "playlist.m3u"
    )

    # --------------------------------------------------------
    # Fetch
    # --------------------------------------------------------

    entries = load_sources()

    print()
    print(
        "========================================"
    )
    print(
        "SOURCE RESULT"
    )
    print(
        "========================================"
    )

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
                "",
            )
        )

        if not url:
            continue

        key = url_key(
            url
        )

        if key in seen_urls:

            duplicate_count += 1

            continue

        seen_urls.add(
            key
        )

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
    # GROUPS
    # --------------------------------------------------------

    grouped = {
        group: []
        for group in GROUPS
    }

    for entry in unique_entries:

        group = group_channel(
            entry
        )

        if group not in grouped:
            group = "Entertainment"

        grouped[
            group
        ].append(
            entry
        )

    # --------------------------------------------------------
    # SORT CHANNELS
    # --------------------------------------------------------

    for group in GROUPS:

        grouped[group].sort(
            key=lambda entry: (
                normalize_text(
                    channel_name(
                        entry
                    )
                ),
                url_key(
                    entry.get(
                        "url",
                        "",
                    )
                ),
            )
        )

    # --------------------------------------------------------
    # WRITE
    # --------------------------------------------------------

    lines = [
        "#EXTM3U",
    ]

    total = 0

    for group in GROUPS:

        for entry in grouped[
            group
        ]:

            lines.append(
                build_extinf(
                    entry,
                    group,
                )
            )

            # Preserve original VLC options.
            for option in entry.get(
                "options",
                [],
            ):
                lines.append(
                    option
                )

            lines.append(
                clean_text(
                    entry["url"]
                )
            )

            total += 1

    output_file.write_text(
        "\n".join(
            lines
        )
        + "\n",
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # REPORT
    # --------------------------------------------------------

    print()
    print(
        "========================================"
    )
    print(
        "PLAYLIST COMPLETE"
    )
    print(
        "========================================"
    )

    print(
        f"Final streams : {total}"
    )

    print(
        f"Output        : {output_file}"
    )

    print()

    for group in GROUPS:

        print(
            f"{group:16} : "
            f"{len(grouped[group])}"
        )


if __name__ == "__main__":
    main()
