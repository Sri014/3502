#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import urllib.request
from collections import OrderedDict

CHANNELS_URL = "https://iptv-org.github.io/api/channels.json"
STREAMS_URL = "https://iptv-org.github.io/api/streams.json"
OUTPUT = "playlist.m3u"

UA = "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 Chrome/151 Safari/537.36"

GROUPS = [
    "India - Hindi",
    "India - English",
    "India - Bhojpuri",
    "India - Music",
    "India - News",
    "India - Lifestyle",
    "India - Infotainment",
    "India - Science",
    "India - Kids",
    "India - Entertainment",
    "UK - Hindi",
    "USA - Hindi",
    "Canada - Hindi",
    "Middle East - Hindi",
    "Sports - Cricket",
    "Radio - Hindi",
]

# ------------------------------------------------------------
# ONLY VERIFIED FOREIGN HINDI CHANNEL NAMES
# ------------------------------------------------------------

FOREIGN_NAMES = {
    "UK": {
        "colors rishtey",
        "colors cineplex",
        "colors tv",
        "sony max",
        "sony sab",
        "sony entertainment television asia",
        "sony sab asia",
        "utsav plus",
        "utsav bharat",
        "zee tv",
        "zee cinema",
        "zee punjabi",
        "star plus",
        "star bharat",
    },
    "USA": {
        "colors tv",
        "colors cineplex",
        "sony max",
        "sony sab",
        "sony pal",
        "sony entertainment television",
        "zee tv",
        "zee cinema",
        "star plus",
        "star bharat",
    },
    "CANADA": {
        "colors tv",
        "colors cineplex",
        "sony max",
        "sony sab",
        "zee tv canada",
        "zee cinema",
        "star plus",
        "star bharat",
        "tag tv",
    },
    "MIDDLE EAST": {
        "colors tv",
        "colors cineplex",
        "sony max",
        "sony sab",
        "zee tv",
        "zee cinema",
        "star plus",
        "star bharat",
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
# FORBIDDEN
# ------------------------------------------------------------

FORBIDDEN = (
    "swayam prabha",
    "pm e-vidya",
    "pm evidya",
    "pm-evidya",
    "vande gujarat",
)

# ------------------------------------------------------------
# INDIA CATEGORY MAP
# ------------------------------------------------------------

CATEGORY_MAP = {
    "music": "India - Music",
    "news": "India - News",
    "lifestyle": "India - Lifestyle",
    "infotainment": "India - Infotainment",
    "science": "India - Science",
    "kids": "India - Kids",
    "entertainment": "India - Entertainment",
}

# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def norm(value):
    value = str(value or "").lower()
    value = value.replace("&amp;", "&")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def fetch_json(url):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "application/json",
        },
    )

    with urllib.request.urlopen(req, timeout=90) as response:
        return json.loads(response.read().decode("utf-8"))


def channel_name(channel):
    return norm(channel.get("name", ""))


def channel_languages(channel):
    return {
        norm(x)
        for x in (channel.get("languages") or [])
    }


def channel_categories(channel):
    return {
        norm(x)
        for x in (channel.get("categories") or [])
    }


def forbidden(name):
    n = norm(name)
    return any(x in n for x in FORBIDDEN)


# ------------------------------------------------------------
# INDIA
# ------------------------------------------------------------

def india_group(channel):
    if norm(channel.get("country")) != "in":
        return None

    name = channel_name(channel)

    if forbidden(name):
        return None

    langs = channel_languages(channel)
    cats = channel_categories(channel)

    # ONLY these 3 languages
    if "hin" in langs:
        return "India - Hindi"

    if "eng" in langs:
        return "India - English"

    if "bho" in langs:
        return "India - Bhojpuri"

    # Categories
    for category, group in CATEGORY_MAP.items():
        if category in cats:
            return group

    return None


# ------------------------------------------------------------
# FOREIGN HINDI
# ------------------------------------------------------------

def foreign_group(channel):
    country = norm(channel.get("country")).upper()
    name = channel_name(channel)

    for region, countries in FOREIGN_COUNTRIES.items():

        if country not in countries:
            continue

        allowed = FOREIGN_NAMES[region]

        if name not in allowed:
            continue

        # Must actually be Hindi
        langs = channel_languages(channel)

        if "hin" not in langs:
            continue

        return f"{region} - Hindi"

    return None


# ------------------------------------------------------------
# CRICKET ONLY
# ------------------------------------------------------------

CRICKET_TERMS = (
    "cricket",
    "willow",
    "fox cricket",
    "supersport cricket",
    "super sport cricket",
)


def cricket_group(channel, stream):
    name = channel_name(channel)

    stream_name = norm(
        " ".join(
            str(stream.get(k, "") or "")
            for k in ("title", "label", "feed")
        )
    )

    text = f"{name} {stream_name}"

    if any(term in text for term in CRICKET_TERMS):
        return "Sports - Cricket"

    return None


# ------------------------------------------------------------
# M3U ENTRY
# ------------------------------------------------------------

def make_entry(channel, stream, group):
    url = str(stream.get("url") or "").strip()

    if not url:
        return None

    name = str(
        channel.get("name")
        or stream.get("title")
        or "Unknown"
    ).strip()

    if forbidden(name):
        return None

    logo = str(channel.get("logo") or "").strip()
    cid = str(channel.get("id") or "").strip()

    lines = [
        (
            f'#EXTINF:-1 tvg-id="{cid}" '
            f'tvg-name="{name}" '
            f'tvg-logo="{logo}" '
            f'group-title="{group}",{name}'
        )
    ]

    referrer = stream.get("referrer")
    user_agent = stream.get("user_agent")

    if referrer:
        lines.append(
            f"#EXTVLCOPT:http-referrer={referrer}"
        )

    if user_agent:
        lines.append(
            f"#EXTVLCOPT:http-user-agent={user_agent}"
        )

    lines.append(url)

    return "\n".join(lines)


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def main():

    print("=" * 60)
    print("FINAL IPTV PLAYLIST GENERATOR")
    print("=" * 60)

    print("[1] Fetch channels...")
    channels_data = fetch_json(CHANNELS_URL)
    print("    Channels:", len(channels_data))

    print("[2] Fetch streams...")
    streams_data = fetch_json(STREAMS_URL)
    print("    Streams :", len(streams_data))

    channels = {}

    for channel in channels_data:

        cid = channel.get("id")

        if not cid:
            continue

        if channel.get("is_nsfw"):
            continue

        if channel.get("closed"):
            continue

        channels[cid] = channel

    groups = OrderedDict(
        (group, [])
        for group in GROUPS
    )

    seen_urls = set()

    duplicate_urls = 0
    dropped = 0

    # --------------------------------------------------------
    # PROCESS STREAMS
    # --------------------------------------------------------

    for stream in streams_data:

        url = str(stream.get("url") or "").strip()

        if not url:
            continue

        # Exact URL duplicate only
        if url in seen_urls:
            duplicate_urls += 1
            continue

        cid = stream.get("channel")

        if not cid:
            dropped += 1
            continue

        channel = channels.get(cid)

        if not channel:
            dropped += 1
            continue

        name = channel.get("name", "")

        if forbidden(name):
            dropped += 1
            continue

        group = None

        # India
        group = india_group(channel)

        # Foreign verified Hindi
        if group is None:
            group = foreign_group(channel)

        # Cricket ONLY
        if group is None:
            group = cricket_group(channel, stream)

        # Unknown = DROP
        if group is None:
            dropped += 1
            continue

        entry = make_entry(
            channel,
            stream,
            group
        )

        if not entry:
            dropped += 1
            continue

        seen_urls.add(url)

        groups[group].append({
            "name": str(name),
            "url": url,
            "entry": entry,
        })

    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    for group in groups:
        groups[group].sort(
            key=lambda x: (
                norm(x["name"]),
                x["url"]
            )
        )

    # --------------------------------------------------------
    # WRITE
    # --------------------------------------------------------

    total = 0

    with open(
        OUTPUT,
        "w",
        encoding="utf-8"
    ) as f:

        f.write("#EXTM3U\n")

        for group, items in groups.items():

            if not items:
                continue

            f.write(
                f"\n# ===== {group} =====\n"
            )

            for item in items:
                f.write(item["entry"])
                f.write("\n")
                total += 1

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("RESULT")
    print("=" * 60)

    for group, items in groups.items():
        print(
            f"{group:<28} {len(items):>5}"
        )

    print("-" * 60)
    print(
        f"TOTAL                    {total:>5}"
    )
    print(
        f"EXACT URL DUPLICATES     {duplicate_urls:>5}"
    )
    print(
        f"DROPPED / UNKNOWN        {dropped:>5}"
    )
    print(
        f"OUTPUT                   {OUTPUT}"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()
