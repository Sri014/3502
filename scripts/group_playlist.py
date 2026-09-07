#!/usr/bin/env python3

import re
import json
import urllib.request
from pathlib import Path


# ============================================================
# IPTV-ORG SOURCES
# ============================================================

SOURCE_URLS = [

    # ========================================================
    # INDIA / REQUIRED LANGUAGE SOURCES
    # ========================================================

    "https://iptv-org.github.io/iptv/languages/hin.m3u",
    "https://iptv-org.github.io/iptv/languages/bho.m3u",
    "https://iptv-org.github.io/iptv/languages/eng.m3u",

    # ========================================================
    # REQUIRED CATEGORIES
    # ========================================================

    "https://iptv-org.github.io/iptv/categories/sports.m3u",
    "https://iptv-org.github.io/iptv/categories/kids.m3u",
    "https://iptv-org.github.io/iptv/categories/entertainment.m3u",
    "https://iptv-org.github.io/iptv/categories/science.m3u",
    "https://iptv-org.github.io/iptv/categories/lifestyle.m3u",

    # ========================================================
    # FOREIGN HINDI ONLY
    #
    # Country playlists are NOT loaded.
    # They are fetched only to pick explicit Hindi allowlist
    # channels below.
    # ========================================================

    "https://iptv-org.github.io/iptv/countries/uk.m3u",
    "https://iptv-org.github.io/iptv/countries/us.m3u",
    "https://iptv-org.github.io/iptv/countries/ca.m3u",

    # Middle East sources only for allowlisted Hindi channels
    "https://iptv-org.github.io/iptv/countries/ae.m3u",
    "https://iptv-org.github.io/iptv/countries/qa.m3u",
    "https://iptv-org.github.io/iptv/countries/sa.m3u",
]


# ============================================================
# FOREIGN HINDI ALLOWLIST
#
# ONLY these foreign/broadcast-area Hindi channels can enter
# from UK / USA / Canada / Middle East country playlists.
#
# No random country channels.
# ============================================================

FOREIGN_HINDI_ALLOWLIST = {

    # ---------------- UK ----------------

    "utsav plus",
    "utsav bharat",
    "sony max",
    "sony max uk",
    "sony sab",
    "sony sab uk",
    "sony entertainment television asia",
    "sony sab asia",

    # ---------------- USA ----------------

    "sony sab usa",
    "sony max us",
    "sony entertainment television",
    "sony pal",

    # ---------------- CANADA ----------------

    "zee tv canada",
    "tag tv",

    # ---------------- MIDDLE EAST ----------------

    "zee cinema",
    "&tv",
    "and tv",
}


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
# RADIO GARDEN
# ============================================================

RADIO_GARDEN_SEARCH_URLS = [

    "https://radio.garden/api/search?q=Hindi",

    "https://radio.garden/api/search?q=Hindi%20Radio",

    "https://radio.garden/api/search?q=Bollywood",

    "https://radio.garden/api/search?q=Hindi%20FM",

]


# Radio Garden direct channel endpoint.
#
# The channel ID is discovered from the Radio Garden API.
# The endpoint redirects to the station's current stream.
# ============================================================

RADIO_GARDEN_STREAM_TEMPLATE = (
    "https://radio.garden/api/ara/content/listen/"
    "{channel_id}/channel.mp3"
)


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

def fetch_bytes(url):

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

        return response.read()


def fetch_text(url):

    data = fetch_bytes(url)

    for encoding in (
        "utf-8-sig",
        "utf-8",
        "latin-1",
    ):

        try:

            return data.decode(
                encoding
            )

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

        value = value.replace(
            old,
            new
        )

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


def normalize_text(value):

    value = clean_text(
        value
    ).lower()

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
                    line[
                        comma + 1:
                    ]
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

            return clean_text(
                value
            )

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
# REMOVE
# ============================================================

REMOVE_WORDS = (

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
# FOREIGN HINDI CHECK
# ============================================================

def is_foreign_hindi(entry):

    name = normalize_text(
        channel_name(entry)
    )

    group = normalize_text(
        channel_group(entry)
    )

    combined = name + " " + group

    for allowed in FOREIGN_HINDI_ALLOWLIST:

        allowed_normalized = normalize_text(
            allowed
        )

        if (
            name == allowed_normalized
            or allowed_normalized in name
        ):

            return True

    # Strong Hindi metadata check for explicitly named
    # foreign/broadcast-area channels.

    if "hindi" in combined:

        for allowed in FOREIGN_HINDI_ALLOWLIST:

            allowed_normalized = normalize_text(
                allowed
            )

            if allowed_normalized in name:

                return True

    return False


# ============================================================
# SPORTS GROUPING
# ============================================================

def sports_group(name, group):

    text = normalize_text(
        name + " " + group
    )

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


    if any(word in text for word in (
        "hockey",
        "nhl",
        "field hockey",
        "ice hockey",
    )):

        return "Sports - Hockey"


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


    if any(word in text for word in (
        "wwe",
        "world wrestling",
        "wrestling",
        "raw",
        "smackdown",
    )):

        return "Sports - WWE"


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

    if is_removed(entry):

        return None


    name = normalize_text(
        channel_name(entry)
    )

    original = normalize_text(
        channel_group(entry)
    )

    combined = (
        name
        + " "
        + original
    )


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

    name = channel_name(
        entry
    )

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
# RADIO GARDEN HELPERS
# ============================================================

def recursive_objects(value):

    if isinstance(
        value,
        dict
    ):

        yield value

        for child in value.values():

            yield from recursive_objects(
                child
            )

    elif isinstance(
        value,
        list
    ):

        for child in value:

            yield from recursive_objects(
                child
            )


def get_first_string(
    obj,
    keys
):

    if not isinstance(
        obj,
        dict
    ):

        return ""

    for key in keys:

        value = obj.get(
            key
        )

        if isinstance(
            value,
            str
        ) and value.strip():

            return clean_text(
                value
            )

    return ""


def radio_is_hindi(obj):

    if not isinstance(
        obj,
        dict
    ):

        return False

    pieces = []

    for key in (
        "name",
        "title",
        "description",
        "language",
        "languages",
        "genre",
        "genres",
        "tags",
        "tag",
        "city",
        "country",
        "place",
    ):

        value = obj.get(
            key
        )

        if isinstance(
            value,
            list
        ):

            pieces.extend(
                str(x)
                for x in value
            )

        elif isinstance(
            value,
            dict
        ):

            pieces.extend(
                str(x)
                for x in value.values()
            )

        elif value is not None:

            pieces.append(
                str(value)
            )

    text = normalize_text(
        " ".join(pieces)
    )

    hindi_words = (
        "hindi",
        "hindustani",
        "bollywood",
        "desi hindi",
        "hindi fm",
        "hindi radio",
        "hindi music",
        "hindi songs",
    )

    return any(
        word in text
        for word in hindi_words
    )


def radio_channel_id(obj):

    if not isinstance(
        obj,
        dict
    ):

        return ""

    possible_keys = (
        "channelId",
        "channel_id",
        "channel",
        "id",
        "slug",
    )

    for key in possible_keys:

        value = obj.get(
            key
        )

        if isinstance(
            value,
            str
        ):

            value = value.strip()

            if value:

                # Avoid accidentally treating place IDs
                # or URLs as channel IDs.
                if (
                    "/" not in value
                    and " " not in value
                ):

                    return value

        elif isinstance(
            value,
            int
        ):

            return str(value)

    return ""


def fetch_radio_garden():

    print()
    print("========================================")
    print("FETCHING HINDI RADIO GARDEN")
    print("========================================")

    stations = []

    seen_ids = set()

    for search_url in RADIO_GARDEN_SEARCH_URLS:

        try:

            raw = fetch_text(
                search_url
            )

            data = json.loads(
                raw
            )

        except Exception as exc:

            print(
                "Radio Garden search FAILED:",
                search_url
            )

            print(
                f"  {type(exc).__name__}: {exc}"
            )

            continue


        found_here = 0

        for obj in recursive_objects(
            data
        ):

            if not radio_is_hindi(
                obj
            ):

                continue

            channel_id = radio_channel_id(
                obj
            )

            if not channel_id:

                continue

            if channel_id in seen_ids:

                continue

            name = get_first_string(
                obj,
                (
                    "name",
                    "title",
                    "stationName",
                    "channelName",
                )
            )

            if not name:

                continue

            city = get_first_string(
                obj,
                (
                    "city",
                    "town",
                    "placeName",
                )
            )

            country = get_first_string(
                obj,
                (
                    "country",
                    "countryName",
                )
            )

            stream_url = (
                RADIO_GARDEN_STREAM_TEMPLATE.format(
                    channel_id=channel_id
                )
            )

            entry = {
                "name": name,
                "url": stream_url,
                "attrs": {
                    "tvg-id": (
                        "radiogarden-"
                        + channel_id
                    ),
                    "tvg-name": name,
                    "radio": "true",
                },
                "options": [],
            }

            if city:

                entry["attrs"][
                    "tvg-city"
                ] = city

            if country:

                entry["attrs"][
                    "tvg-country"
                ] = country

            stations.append(
                entry
            )

            seen_ids.add(
                channel_id
            )

            found_here += 1


        print(
            f"{search_url:55} "
            f"{found_here:4} Hindi stations"
        )


    print(
        f"Radio Garden total : "
        f"{len(stations)}"
    )

    return stations


# ============================================================
# LOAD IPTV SOURCES
# ============================================================

def load_sources():

    all_entries = []

    print()
    print("========================================")
    print("FETCHING IPTV SOURCES")
    print("========================================")

    for url in SOURCE_URLS:

        filename = url.rsplit(
            "/",
            1
        )[-1]

        try:

            text = fetch_text(
                url
            )

            entries = parse_m3u(
                text
            )

            print(
                f"{filename:35} "
                f"{len(entries):5} channels"
            )

            # ------------------------------------------------
            # IMPORTANT:
            # Foreign country feeds are allowlist filtered.
            # ------------------------------------------------

            is_foreign_source = any(
                country in url
                for country in (
                    "/countries/uk.m3u",
                    "/countries/us.m3u",
                    "/countries/ca.m3u",
                    "/countries/ae.m3u",
                    "/countries/qa.m3u",
                    "/countries/sa.m3u",
                )
            )

            if is_foreign_source:

                allowed = []

                for entry in entries:

                    if is_removed(
                        entry
                    ):

                        continue

                    if is_foreign_hindi(
                        entry
                    ):

                        allowed.append(
                            entry
                        )

                print(
                    f"  FOREIGN HINDI ALLOWED: "
                    f"{len(allowed)}"
                )

                all_entries.extend(
                    allowed
                )

            else:

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


    # ========================================================
    # RADIO GARDEN
    # ========================================================

    radio_entries = fetch_radio_garden()

    all_entries.extend(
        radio_entries
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


    # ========================================================
    # EXACT URL DEDUP
    #
    # Same URL -> one entry
    # Same channel + different URL -> BOTH KEPT
    # ========================================================

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

        key = url.strip().lower()

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


    # ========================================================
    # GROUP
    # ========================================================

    grouped = {
        group: []
        for group in GROUPS
    }

    removed = 0

    for entry in unique_entries:

        group = group_channel(
            entry
        )

        # Radio Garden entries must always remain Radio.
        if (
            str(
                entry.get(
                    "attrs",
                    {}
                ).get(
                    "radio",
                    ""
                )
            ).lower()
            == "true"
        ):

            group = "Radio"


        if group is None:

            removed += 1

            continue

        if group not in grouped:

            group = "Entertainment"

        grouped[group].append(
            entry
        )


    # ========================================================
    # SORT
    # ========================================================

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


    # ========================================================
    # BUILD PLAYLIST
    # ========================================================

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

                lines.append(
                    option
                )

            lines.append(
                clean_text(
                    entry["url"]
                )
            )

            total += 1


    # ========================================================
    # WRITE
    # ========================================================

    output_file.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


    # ========================================================
    # RESULT
    # ========================================================

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
