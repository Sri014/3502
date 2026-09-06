#!/usr/bin/env python3

"""
Group and merge IPTV M3U playlists.

Rules:
- Duplicate streams are NOT removed.
- Every valid source entry is retained.
- Existing group-title is preserved when useful.
- Language/region/category are normalized.
- Tata Play / JioTV style categories are preserved.
- Indian channels found in foreign sources are retained.
- Sports/news/kids/infotainment/science/lifestyle/etc. are not discarded.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


CATEGORY_ALIASES = {
    "infotainment": "Infotainment",
    "documentary": "Documentary",
    "documentaries": "Documentary",
    "science": "Science",
    "lifestyle": "Lifestyle",
    "life style": "Lifestyle",
    "entertainment": "Entertainment",
    "movies": "Movies",
    "movie": "Movies",
    "music": "Music",
    "news": "News",
    "sports": "Sports",
    "sport": "Sports",
    "kids": "Kids",
    "children": "Kids",
    "cartoons": "Kids",
    "business": "Business",
    "devotional": "Devotional",
    "religious": "Devotional",
    "education": "Education",
    "educational": "Education",
    "travel": "Travel",
    "food": "Food",
    "cooking": "Food",
    "shopping": "Shopping",
    "regional": "Regional",
    "general": "General",
    "reality": "Reality",
    "anime": "Anime",
    "horror": "Horror",
    "comedy": "Comedy",
    "weather": "Weather",
}


LANGUAGE_WORDS = {
    "hindi": "Hindi",
    "bhojpuri": "Bhojpuri",
    "english": "English",
    "tamil": "Tamil",
    "telugu": "Telugu",
    "malayalam": "Malayalam",
    "kannada": "Kannada",
    "marathi": "Marathi",
    "bengali": "Bengali",
    "bangla": "Bengali",
    "punjabi": "Punjabi",
    "gujarati": "Gujarati",
    "odia": "Odia",
    "assamese": "Assamese",
    "urdu": "Urdu",
}


COUNTRY_WORDS = {
    "india": "India",
    "indian": "India",
    "usa": "USA",
    "us": "USA",
    "america": "USA",
    "uk": "UK",
    "britain": "UK",
    "united kingdom": "UK",
    "canada": "Canada",
    "australia": "Australia",
    "uae": "UAE",
    "dubai": "UAE",
    "singapore": "Singapore",
    "malaysia": "Malaysia",
    "nepal": "Nepal",
    "bangladesh": "Bangladesh",
    "pakistan": "Pakistan",
    "south africa": "South Africa",
}


def clean(value: str) -> str:
    value = value.strip()
    value = value.replace("\\,", ",")
    value = re.sub(r"\s+", " ", value)
    return value


def parse_attributes(line: str) -> dict[str, str]:
    attrs = {}

    for match in re.finditer(
        r'([\w-]+)="([^"]*)"', line
    ):
        attrs[match.group(1)] = clean(match.group(2))

    return attrs


def replace_attribute(line: str, key: str, value: str) -> str:
    pattern = rf'({re.escape(key)}=")[^"]*(")'

    if re.search(pattern, line):
        return re.sub(
            pattern,
            lambda m: m.group(1) + value + m.group(2),
            line,
            count=1,
        )

    # Insert before the channel name.
    return line.replace(
        "#EXTINF:-1",
        f'#EXTINF:-1 {key}="{value}"',
        1,
    )


def normalize_category(raw: str, name: str) -> str:
    text = f"{raw} {name}".lower()

    for key, category in CATEGORY_ALIASES.items():
        if re.search(rf"\b{re.escape(key)}\b", text):
            return category

    return clean(raw) if raw else "General"


def detect_language(group: str, name: str) -> str:
    text = f"{group} {name}".lower()

    # Check longer/more specific words first.
    for key in sorted(LANGUAGE_WORDS, key=len, reverse=True):
        if re.search(rf"\b{re.escape(key)}\b", text):
            return LANGUAGE_WORDS[key]

    return ""


def detect_country(group: str, name: str) -> str:
    text = f"{group} {name}".lower()

    for key in sorted(COUNTRY_WORDS, key=len, reverse=True):
        if re.search(rf"\b{re.escape(key)}\b", text):
            return COUNTRY_WORDS[key]

    return ""


def make_group(attrs: dict[str, str]) -> str:
    name = attrs.get("tvg-name", "").strip()
    old_group = attrs.get("group-title", "").strip()

    category = normalize_category(
        old_group,
        name,
    )

    language = detect_language(
        old_group,
        name,
    )

    country = detect_country(
        old_group,
        name,
    )

    # Preserve useful existing groups such as:
    # Tata Play / JioTV category names.
    if old_group:
        old_lower = old_group.lower()

        # If the existing group already looks meaningful,
        # keep it instead of throwing it away.
        for marker in (
            "tata",
            "jiotv",
            "jio",
            "bhojpuri",
            "hindi",
            "english",
            "sports",
            "news",
            "kids",
            "science",
            "lifestyle",
            "infotainment",
        ):
            if marker in old_lower:
                return old_group

    if language and country:
        return f"{language} - {country} - {category}"

    if language:
        return f"{language} - {category}"

    if country:
        return f"{country} - {category}"

    return category


def read_m3u(path: Path) -> list[tuple[str, str]]:
    entries = []

    lines = path.read_text(
        encoding="utf-8",
        errors="replace",
    ).splitlines()

    extinf = None

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("#EXTINF:"):
            extinf = line
            continue

        if extinf and not line.startswith("#"):
            entries.append((extinf, line))
            extinf = None

    return entries


def process_file(path: Path) -> list[tuple[str, str]]:
    result = []

    for extinf, url in read_m3u(path):
        attrs = parse_attributes(extinf)

        name = attrs.get("tvg-name", "").strip()

        if not name:
            # Try channel name after the last comma.
            if "," in extinf:
                name = clean(extinf.rsplit(",", 1)[1])

        if not url:
            continue

        # Keep every stream.
        # No URL-based duplicate removal here.
        group = make_group(
            {
                **attrs,
                "tvg-name": name,
            }
        )

        new_extinf = replace_attribute(
            extinf,
            "group-title",
            group,
        )

        result.append((new_extinf, url))

    return result


def collect_files(source: Path) -> list[Path]:
    if source.is_file():
        return [source]

    return sorted(
        p
        for p in source.rglob("*.m3u")
        if p.is_file()
    )


def build(source: Path, output: Path) -> None:
    files = collect_files(source)

    all_entries = []

    for playlist in files:
        print(f"[+] Reading: {playlist}")

        try:
            entries = process_file(playlist)
            all_entries.extend(entries)
            print(f"    {len(entries)} streams")
        except Exception as exc:
            print(f"[!] Failed: {playlist}: {exc}")

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output.open(
        "w",
        encoding="utf-8",
        newline="\n",
    ) as fh:
        fh.write("#EXTM3U\n")

        for extinf, url in all_entries:
            fh.write(extinf + "\n")
            fh.write(url + "\n")

    print()
    print("================================")
    print(f"Input playlists : {len(files)}")
    print(f"Total streams   : {len(all_entries)}")
    print(f"Output          : {output}")
    print("Duplicates      : KEPT")
    print("================================")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Merge and intelligently group M3U playlists."
    )

    parser.add_argument(
        "source",
        nargs="?",
        default="sources",
        help="M3U file or directory containing M3U files",
    )

    parser.add_argument(
        "-o",
        "--output",
        default="playlist.m3u",
        help="Output M3U file",
    )

    args = parser.parse_args()

    build(
        Path(args.source),
        Path(args.output),
    )


if __name__ == "__main__":
    main()
