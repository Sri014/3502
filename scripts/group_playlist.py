#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import urllib.request
import urllib.parse
from collections import OrderedDict

CHANNELS_URL = "https://iptv-org.github.io/api/channels.json"
STREAMS_URL = "https://iptv-org.github.io/api/streams.json"

OUTPUT = "playlist.m3u"

UA = (
    "Mozilla/5.0 (Linux; Android 10) "
    "AppleWebKit/537.36 Chrome/151.0 Mobile Safari/537.36"
)

# ------------------------------------------------------------
# FOREIGN VERIFIED HINDI
# ------------------------------------------------------------

FOREIGN = {
    "UK": {
        "utsav plus",
        "utsav bharat",
        "sony max",
        "sony max uk",
        "sony sab",
        "sony sab uk",
        "sony entertainment television asia",
        "sony sab asia",
    },

    "USA": {
        "sony sab usa",
        "sony max us",
        "sony entertainment television",
        "sony pal",
    },

    "CANADA": {
        "zee tv canada",
        "tag tv",
    },

    "MIDDLE EAST": {
        "zee cinema",
        "and tv",
        "&tv",
    },
}

FOREIGN_COUNTRIES = {
    "UK": {"GB", "UK"},
    "USA": {"US"},
    "CANADA": {"CA"},
    "MIDDLE EAST": {"AE", "QA", "SA", "BH", "KW", "OM"},
}

# ------------------------------------------------------------
# INDIA CATEGORIES
# ------------------------------------------------------------

INDIA_GROUPS = {
    "hin": "India - Hindi",
    "eng": "India - English",
    "bho": "India - Bhojpuri",
}

INDIA_CATEGORIES = {
    "kids": "India - Kids",
    "entertainment": "India - Entertainment",
    "information": "India - Information",
    "science": "India - Science",
    "lifestyle": "India - Lifestyle",
}

# ------------------------------------------------------------
# SPORTS
# ------------------------------------------------------------

SPORT_TERMS = {
    "Cricket": [
        "cricket",
        "willow",
        "fox cricket",
        "supersport cricket",
    ],

    "Hockey": [
        "hockey",
        "nhl",
    ],

    "Football": [
        "football",
        "soccer",
        "sky sports",
        "tnt sports",
        "espn",
        "fox sports",
        "bein sports",
    ],

    "WWE": [
        "wwe",
        "wwf",
    ],

    "Tennis": [
        "tennis",
        "atp",
        "wta",
        "eurosport",
    ],
}

SPORT_PROVIDER_TERMS = [
    "willow",
    "super sport",
    "supersport",
    "sky sports",
    "tnt sports",
    "fox sports",
    "fox cricket",
    "espn",
    "eurosport",
    "bein sports",
]

# ------------------------------------------------------------
# REMOVE THESE COMPLETELY
# ------------------------------------------------------------

REMOVE_WORDS = [
    "swayam prabha",
    "pm e-vidya",
    "pm evidya",
    "pm-evidya",
    "vande gujarat",
]

# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def fetch_json(url):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "application/json",
        },
    )

    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def clean(text):
    text = str(text or "").lower()
    text = text.replace("&amp;", "&")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def channel_text(ch):
    values = []

    values.append(ch.get("name", ""))

    for x in ch.get("alt_names", []) or []:
        values.append(x)

    values.append(ch.get("network", ""))

    return clean(" ".join(map(str, values)))


def stream_text(stream):
    return clean(
        " ".join(
            str(x or "")
            for x in [
                stream.get("title"),
                stream.get("label"),
                stream.get("feed"),
            ]
        )
    )


def blocked_name(text):
    t = clean(text)

    return any(word in t for word in REMOVE_WORDS)


def is_india(ch):
    return clean(ch.get("country")) == "in"


def has_category(ch, category):
    categories = {
        clean(x)
        for x in (ch.get("categories") or [])
    }

    return category.lower() in categories


def languages(ch):
    return {
        clean(x)
        for x in (ch.get("languages") or [])
    }


def foreign_group(ch):
    name = channel_text(ch)
    country = clean(ch.get("country")).upper()

    for group, names in FOREIGN.items():

        if country not in FOREIGN_COUNTRIES[group]:
            continue

        if name in names:
            return group

        # Exact-ish normalized matching for names with suffixes
        for allowed in names:
            if name == allowed:
                return group

    return None


def sport_group(ch, stream):
    text = " ".join([
        channel_text(ch),
        stream_text(stream),
    ])

    # Only requested sports.
    for sport, terms in SPORT_TERMS.items():

        for term in terms:
            if term in text:
                return f"Sports - {sport}"

    return None


def india_group(ch):
    if not is_india(ch):
        return None

    name = channel_text(ch)

    if blocked_name(name):
        return None

    langs = languages(ch)

    cats = {
        clean(x)
        for x in (ch.get("categories") or [])
    }

    # Hindi
    if "hin" in langs:
        return "India - Hindi"

    # Bhojpuri
    if "bho" in langs:
        return "India - Bhojpuri"

    # English
    if "eng" in langs:
        return "India - English"

    # Required Indian categories
    for category, group in INDIA_CATEGORIES.items():
        if category in cats:
            return group

    return None


# ------------------------------------------------------------
# PLAYLIST ENTRY
# ------------------------------------------------------------

def make_entry(ch, stream, group):
    name = ch.get("name") or stream.get("title") or "Unknown"

    logo = ch.get("logo") or ""

    url = str(stream.get("url") or "").strip()

    if not url:
        return None

    if blocked_name(name):
        return None

    # Don't include obviously dead/blocked labels.
    label = clean(stream.get("label"))

    if any(x in label for x in [
        "blocked",
        "dmca",
        "retired",
    ]):
        return None

    entry = [
        f'#EXTINF:-1 tvg-id="{ch.get("id", "")}" '
        f'tvg-name="{name}" '
        f'tvg-logo="{logo}" '
        f'group-title="{group}",{name}'
    ]

    referrer = stream.get("referrer")
    user_agent = stream.get("user_agent")

    if referrer:
        entry.append(f"#EXTVLCOPT:http-referrer={referrer}")

    if user_agent:
        entry.append(f"#EXTVLCOPT:http-user-agent={user_agent}")

    entry.append(url)

    return "\n".join(entry)


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def main():

    print("=" * 60)
    print(" IPTV PLAYLIST GENERATOR")
    print("=" * 60)

    print("[1/4] Fetching channels.json...")
    channels_data = fetch_json(CHANNELS_URL)

    print(f"      Channels fetched: {len(channels_data):,}")

    print("[2/4] Fetching streams.json...")
    streams_data = fetch_json(STREAMS_URL)

    print(f"      Streams fetched:  {len(streams_data):,}")

    # --------------------------------------------------------
    # Channel lookup
    # --------------------------------------------------------

    channels = {}

    for ch in channels_data:

        cid = ch.get("id")

        if not cid:
            continue

        if ch.get("is_nsfw"):
            continue

        if ch.get("closed"):
            continue

        channels[cid] = ch

    # --------------------------------------------------------
    # Build playlist
    # --------------------------------------------------------

    groups = OrderedDict()

    for group in [
        "India - Hindi",
        "India - English",
        "India - Bhojpuri",
        "India - Kids",
        "India - Entertainment",
        "India - Information",
        "India - Science",
        "India - Lifestyle",
        "UK - Hindi",
        "USA - Hindi",
        "Canada - Hindi",
        "Middle East - Hindi",
        "Sports - Cricket",
        "Sports - Hockey",
        "Sports - Football",
        "Sports - WWE",
        "Sports - Tennis",
        "Radio - Hindi",
    ]:
        groups[group] = []

    # Exact URL duplicate protection.
    seen_urls = set()

    duplicate_urls = 0
    dropped = 0

    for stream in streams_data:

        url = str(stream.get("url") or "").strip()

        if not url:
            continue

        # EXACT SAME URL = remove duplicate
        if url in seen_urls:
            duplicate_urls += 1
            continue

        cid = stream.get("channel")

        if not cid:
            dropped += 1
            continue

        ch = channels.get(cid)

        if not ch:
            dropped += 1
            continue

        name = ch.get("name") or stream.get("title") or ""

        if blocked_name(name):
            dropped += 1
            continue

        group = None

        # ----------------------------------------------------
        # INDIA
        # ----------------------------------------------------

        group = india_group(ch)

        # ----------------------------------------------------
        # FOREIGN VERIFIED HINDI
        # ----------------------------------------------------

        if group is None:
            fg = foreign_group(ch)

            if fg:
                group = f"{fg} - Hindi"

        # ----------------------------------------------------
        # SPORTS
        # ----------------------------------------------------

        if group is None:
            group = sport_group(ch, stream)

        # ----------------------------------------------------
        # IMPORTANT:
        # NO FALLBACK TO ENTERTAINMENT.
        # UNKNOWN CHANNELS ARE DROPPED.
        # ----------------------------------------------------

        if group is None:
            dropped += 1
            continue

        entry = make_entry(ch, stream, group)

        if not entry:
            dropped += 1
            continue

        seen_urls.add(url)

        groups[group].append({
            "name": name,
            "url": url,
            "entry": entry,
        })

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    for group in groups:
        groups[group].sort(
            key=lambda x: (
                clean(x["name"]),
                x["url"],
            )
        )

    # --------------------------------------------------------
    # Write M3U
    # --------------------------------------------------------

    total = 0

    with open(OUTPUT, "w", encoding="utf-8") as f:

        f.write("#EXTM3U\n")

        for group, items in groups.items():

            if not items:
                continue

            f.write(
                f"\n"
                f"# ===== {group} =====\n"
            )

            for item in items:
                f.write(item["entry"])
                f.write("\n")

                total += 1

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print(" PLAYLIST RESULT")
    print("=" * 60)

    for group, items in groups.items():

        if items:
            print(
                f"{group:<25} : {len(items):>5}"
            )

    print("-" * 60)

    print(
        f"TOTAL STREAMS          : {total:,}"
    )

    print(
        f"DUPLICATE URL REMOVED  : {duplicate_urls:,}"
    )

    print(
        f"DROPPED                 : {dropped:,}"
    )

    print(
        f"OUTPUT                  : {OUTPUT}"
    )

    print("=" * 60)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nStopped.")

    except Exception as e:
        print()
        print("ERROR:")
        print(type(e).__name__, str(e))
        raise
