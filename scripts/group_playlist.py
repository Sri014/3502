#!/usr/bin/env python3

import json
import re
import urllib.parse
import urllib.request
from pathlib import Path


# ============================================================
# IPTV-ORG SOURCES
# ============================================================

SOURCE_URLS = [

    # India / required languages
    "https://iptv-org.github.io/iptv/languages/hin.m3u",
    "https://iptv-org.github.io/iptv/languages/bho.m3u",
    "https://iptv-org.github.io/iptv/languages/eng.m3u",

    # Required categories
    "https://iptv-org.github.io/iptv/categories/sports.m3u",
    "https://iptv-org.github.io/iptv/categories/kids.m3u",
    "https://iptv-org.github.io/iptv/categories/entertainment.m3u",
    "https://iptv-org.github.io/iptv/categories/science.m3u",
    "https://iptv-org.github.io/iptv/categories/lifestyle.m3u",

    # Foreign feeds are ONLY used for allowlisted Hindi channels
    "https://iptv-org.github.io/iptv/countries/uk.m3u",
    "https://iptv-org.github.io/iptv/countries/us.m3u",
    "https://iptv-org.github.io/iptv/countries/ca.m3u",
    "https://iptv-org.github.io/iptv/countries/ae.m3u",
    "https://iptv-org.github.io/iptv/countries/qa.m3u",
    "https://iptv-org.github.io/iptv/countries/sa.m3u",
]


# ============================================================
# FOREIGN HINDI ALLOWLIST
# ============================================================
#
# IMPORTANT:
# Country playlist ka koi random channel accept nahi hoga.
# Sirf yahan listed channel hi foreign source se aa sakta hai.
#
# Names ko normalized form me compare kiya jayega.
# ============================================================

FOREIGN_HINDI_ALLOWLIST = {

    # UK
    "utsav plus",
    "utsav bharat",
    "sony max",
    "sony max uk",
    "sony sab",
    "sony sab uk",
    "sony entertainment television asia",
    "sony sab asia",

    # USA
    "sony sab usa",
    "sony max us",
    "sony entertainment television",
    "sony pal",

    # Canada
    "zee tv canada",
    "tag tv",

    # Middle East / wider broadcast area
    "zee cinema",
    "and tv",
    "&tv",
}


# ============================================================
# SPORTS ALLOWLIST / TYPES
# ============================================================

SPORT_TYPES = (
    "cricket",
    "hockey",
    "football",
    "wwe",
    "tennis",
)


# ============================================================
# GROUPS
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

RADIO_GARDEN_SEARCHES = (
    "Hindi",
    "Hindi Radio",
    "Hindi FM",
    "Hindi Music",
    "Bollywood",
)


RADIO_GARDEN_STREAM = (
    "https://radio.garden/api/ara/content/listen/"
    "{}/channel.mp3"
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
            return data.decode(encoding)

        except UnicodeDecodeError:
            pass

    return data.decode(
        "utf-8",
        errors="replace",
    )


def fetch_json(url):

    return json.loads(
        fetch_text(url)
    )


# ============================================================
# TEXT HELPERS
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
# M3U ATTRIBUTES
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
# CHANNEL HELPERS
# ============================================================

def get_attr(entry, *names):

    attrs = entry.get(
        "attrs",
        {},
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
# FOREIGN HINDI FILTER
# ============================================================

def is_foreign_hindi(entry):

    name = normalize_text(
        channel_name(entry)
    )

    attrs = entry.get(
        "attrs",
        {},
    )

    language = normalize_text(
        attrs.get(
            "tvg-language",
            "",
        )
    )

    group = normalize_text(
        channel_group(entry)
    )

    combined = (
        name
        + " "
        + language
        + " "
        + group
    )

    # Exact / contained allowlist match
    for allowed in FOREIGN_HINDI_ALLOWLIST:

        allowed_name = normalize_text(
            allowed
        )

        if (
            name == allowed_name
            or allowed_name in name
        ):

            return True

    # Do NOT accept every channel just because
    # "hindi" appears in its metadata.
    #
    # Hindi metadata is only accepted when channel
    # itself is allowlisted.

    if "hindi" not in combined:
        return False

    return False


# ============================================================
# SPORTS GROUP
# ============================================================

def sports_group(name, group):

    text = normalize_text(
        name + " " + group
    )

    # Cricket
    if any(x in text for x in (
        "cricket",
        "willow",
        "fox cricket",
        "sky cricket",
        "supersport cricket",
        "super sport cricket",
        "ten cricket",
        "sony sports ten 3",
        "sony ten 3",
        "star sports cricket",
        "icc",
    )):

        return "Sports - Cricket"


    # Hockey
    if any(x in text for x in (
        "hockey",
        "nhl",
        "field hockey",
        "ice hockey",
    )):

        return "Sports - Hockey"


    # Football
    if any(x in text for x in (
        "football",
        "soccer",
        "premier league",
        "epl",
        "uefa",
        "champions league",
        "fifa",
        "sky sports football",
        "tnt sports football",
    )):

        return "Sports - Football"


    # WWE
    if any(x in text for x in (
        "wwe",
        "world wrestling",
        "wrestling",
        "raw",
        "smackdown",
    )):

        return "Sports - WWE"


    # Tennis
    if any(x in text for x in (
        "tennis",
        "atp",
        "wta",
        "wimbledon",
        "us open",
        "french open",
        "australian open",
    )):

        return "Sports - Tennis"


    return "Sports"


# ============================================================
# GROUP CHANNEL
# ============================================================

def group_channel(entry):

    if is_removed(entry):
        return None


    name = normalize_text(
        channel_name(entry)
    )

    group = normalize_text(
        channel_group(entry)
    )

    combined = (
        name
        + " "
        + group
    )


    # ========================================================
    # SPORTS
    # ========================================================

    if any(x in combined for x in (
        "cricket",
        "hockey",
        "football",
        "soccer",
        "wwe",
        "tennis",
        "sport",
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
            group,
        )


    # ========================================================
    # BHOJPURI
    # ========================================================

    if any(x in combined for x in (
        "bhojpuri",
        "bhojpuriya",
    )):

        return "Bhojpuri"


    # ========================================================
    # HINDI
    # ========================================================

    if any(x in combined for x in (
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


    # ========================================================
    # ENGLISH
    # ========================================================

    if "english" in combined:
        return "English"


    # ========================================================
    # KIDS
    # ========================================================

    if any(x in combined for x in (
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


    # ========================================================
    # SCIENCE
    # ========================================================

    if any(x in combined for x in (
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


    # ========================================================
    # LIFESTYLE
    # ========================================================

    if any(x in combined for x in (
        "lifestyle",
        "fashion",
        "food",
        "travel",
        "living",
        "home",
        "cooking",
    )):

        return "Lifestyle"


    # ========================================================
    # INFORMATION
    # ========================================================

    if any(x in combined for x in (
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


    # ========================================================
    # ENTERTAINMENT
    # ========================================================

    if any(x in combined for x in (
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
        "'",
    )


def build_extinf(entry, group):

    attrs = entry.get(
        "attrs",
        {},
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
# RADIO GARDEN
# ============================================================

def walk_json(value):

    if isinstance(value, dict):

        yield value

        for child in value.values():

            yield from walk_json(
                child
            )

    elif isinstance(value, list):

        for child in value:

            yield from walk_json(
                child
            )


def radio_text(obj):

    parts = []

    if not isinstance(
        obj,
        dict,
    ):

        return ""


    for key in (
        "name",
        "title",
        "description",
        "language",
        "languages",
        "genre",
        "genres",
        "tags",
        "city",
        "country",
        "place",
    ):

        value = obj.get(key)

        if isinstance(
            value,
            list,
        ):

            parts.extend(
                str(x)
                for x in value
            )

        elif isinstance(
            value,
            dict,
        ):

            parts.extend(
                str(x)
                for x in value.values()
            )

        elif value is not None:

            parts.append(
                str(value)
            )

    return normalize_text(
        " ".join(parts)
    )


def radio_channel_id(obj):

    if not isinstance(
        obj,
        dict,
    ):

        return ""


    # Radio Garden search objects commonly expose
    # channel ID through id/channelId.
    for key in (
        "channelId",
        "channel_id",
    ):

        value = obj.get(key)

        if value:

            return str(
                value
            ).strip()


    # Some API/search representations put ID inside _source.
    source = obj.get(
        "_source"
    )

    if isinstance(
        source,
        dict,
    ):

        for key in (
            "channelId",
            "channel_id",
            "id",
        ):

            value = source.get(key)

            if value:

                return str(
                    value
                ).strip()


    # Direct id is accepted only when this object
    # looks like a station.
    value = obj.get(
        "id"
    )

    if value:

        station_text = radio_text(
            obj
        )

        if any(x in station_text for x in (
            "hindi",
            "bollywood",
            "radio",
            "fm",
        )):

            return str(
                value
            ).strip()


    return ""


def radio_station_name(obj):

    if not isinstance(
        obj,
        dict,
    ):

        return ""


    source = obj.get(
        "_source"
    )

    objects = [obj]

    if isinstance(
        source,
        dict,
    ):

        objects.append(
            source
        )


    for current in objects:

        for key in (
            "name",
            "title",
            "stationName",
            "channelName",
        ):

            value = current.get(
                key
            )

            if (
                isinstance(
                    value,
                    str,
                )
                and value.strip()
            ):

                return clean_text(
                    value
                )


    return ""


def radio_is_hindi(obj):

    text = radio_text(
        obj
    )

    return any(x in text for x in (
        "hindi",
        "hindustani",
        "hindi radio",
        "hindi fm",
        "hindi music",
        "hindi songs",
        "bollywood",
    ))


def fetch_radio_garden():

    print()
    print(
        "========================================"
    )
    print(
        "FETCHING HINDI RADIO GARDEN"
    )
    print(
        "========================================"
    )

    stations = []
    seen_ids = set()

    for query in RADIO_GARDEN_SEARCHES:

        url = (
            "https://radio.garden/api/search?q="
            + urllib.parse.quote(
                query
            )
        )

        try:

            data = fetch_json(
                url
            )

        except Exception as exc:

            print(
                f"Radio Garden [{query}] FAILED: "
                f"{type(exc).__name__}: {exc}"
            )

            continue


        added = 0

        for obj in walk_json(
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


            name = radio_station_name(
                obj
            )

            if not name:

                continue


            stream_url = (
                RADIO_GARDEN_STREAM.format(
                    channel_id
                )
            )


            stations.append({
                "name": name,
                "url": stream_url,
                "attrs": {
                    "tvg-id": (
                        "radio-garden-"
                        + channel_id
                    ),
                    "tvg-name": name,
                    "radio": "true",
                },
                "options": [],
            })


            seen_ids.add(
                channel_id
            )

            added += 1


        print(
            f"{query:20} -> "
            f"{added} Hindi stations"
        )


    print(
        f"Radio Garden total: "
        f"{len(stations)}"
    )

    return stations


# ============================================================
# LOAD SOURCES
# ============================================================

def load_sources():

    all_entries = []

    print()
    print(
        "========================================"
    )
    print(
        "FETCHING IPTV SOURCES"
    )
    print(
        "========================================"
    )


    foreign_paths = (
        "/countries/uk.m3u",
        "/countries/us.m3u",
        "/countries/ca.m3u",
        "/countries/ae.m3u",
        "/countries/qa.m3u",
        "/countries/sa.m3u",
    )


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


            # =================================================
            # FOREIGN:
            # ONLY ALLOWLIST
            # =================================================

            is_foreign = any(
                path in url
                for path in foreign_paths
            )


            if is_foreign:

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
                    f"  -> allowlisted Hindi: "
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


    # ========================================================
    # EXACT URL DEDUP ONLY
    # ========================================================

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


        key = url.lower().strip()


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

        attrs = entry.get(
            "attrs",
            {},
        )


        # Radio Garden is always Radio
        if (
            str(
                attrs.get(
                    "radio",
                    "",
                )
            ).lower()
            == "true"
        ):

            group = "Radio"

        else:

            group = group_channel(
                entry
            )


        if group is None:

            removed += 1

            continue


        if group not in grouped:

            continue


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
                        "",
                    )
                ).lower(),
            )
        )


    # ========================================================
    # BUILD
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
                    group,
                )
            )


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
