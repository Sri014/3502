#!/usr/bin/env python3

import argparse
import gzip
import io
import json
import re
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse


# ============================================================
# CONFIG
# ============================================================

SOURCE_URLS = [
    "https://raw.githubusercontent.com/wizakorhd/iptv/main/playlist-hindi.m3u",
    "https://raw.githubusercontent.com/wizakorhd/iptv/main/playlist-english-india.m3u",
    "https://raw.githubusercontent.com/wizakorhd/iptv/main/playlist-top.m3u",
    "https://raw.githubusercontent.com/wizakorhd/iptv/main/playlist.m3u",
]

JIOTV_JSON_URL = (
    "https://gist.githubusercontent.com/mitthu786/"
    "raw/tsjiotv.json"
)

JIOTV_EPG_URL = (
    "https://raw.githubusercontent.com/mitthu786/tvepg/main/"
    "jiotv/epg.xml.gz"
)

TATAPLAY_EPG_URL = (
    "https://raw.githubusercontent.com/mitthu786/tvepg/main/"
    "tataplay/epg.xml.gz"
)

GROUPS = [
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

ALLOWED_LANGUAGES = {
    "hindi",
    "english",
    "bhojpuri",
}

FOREIGN_CRICKET_WORDS = (
    "cricket",
    "icc",
)

BAD_LANGUAGES = {
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
    "urdu",
    "sinhala",
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
# HTTP
# ============================================================

def fetch_bytes(url, timeout=35):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 "
                "Chrome/140 Safari/537.36"
            ),
            "Accept": "*/*",
        },
    )

    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def fetch_text(url):
    data = fetch_bytes(url)

    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            pass

    return data.decode("utf-8", errors="replace")


# ============================================================
# NORMALIZATION
# ============================================================

def clean_text(value):
    if value is None:
        return ""

    value = str(value)
    value = value.replace("&amp;", "&")
    value = value.replace("&quot;", '"')
    value = value.replace("&#39;", "'")
    value = value.replace("&apos;", "'")

    return re.sub(r"\s+", " ", value).strip()


def normalize_name(value):
    value = clean_text(value).lower()

    value = value.replace("&", " and ")

    value = re.sub(
        r"\b(uhd|4k|8k|fhd|hd|sd|hevc|h265|h264|"
        r"1080p|720p|576p|480p)\b",
        " ",
        value,
        flags=re.I,
    )

    value = re.sub(
        r"\b(india|in)\s*[:\-|]\s*",
        " ",
        value,
        flags=re.I,
    )

    value = re.sub(r"[^a-z0-9]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()

    return value


def compact_name(value):
    return re.sub(r"[^a-z0-9]+", "", normalize_name(value))


def words(value):
    return set(normalize_name(value).split())


# ============================================================
# M3U PARSER
# ============================================================

def parse_m3u(text):
    entries = []

    lines = text.splitlines()

    current = None

    for raw in lines:
        line = raw.strip()

        if not line:
            continue

        if line.startswith("#EXTINF:"):
            current = {
                "extinf": line,
                "url": "",
                "name": "",
                "attrs": {},
            }

            comma = line.find(",")

            if comma >= 0:
                current["name"] = clean_text(line[comma + 1:])

            attrs_part = line[:comma] if comma >= 0 else line

            for match in re.finditer(
                r'([\w-]+)="([^"]*)"',
                attrs_part,
            ):
                current["attrs"][match.group(1)] = match.group(2)

        elif not line.startswith("#") and current is not None:
            current["url"] = line

            if current["url"]:
                entries.append(current)

            current = None

    return entries


def get_attr(entry, *names):
    attrs = entry.get("attrs", {})

    for name in names:
        value = attrs.get(name)

        if value:
            return clean_text(value)

    return ""


# ============================================================
# JIOTV REFERENCE
# ============================================================

def parse_jiotv_json(data):
    result = []

    if isinstance(data, dict):
        for key in (
            "channels",
            "data",
            "results",
            "items",
        ):
            if isinstance(data.get(key), list):
                data = data[key]
                break

    if not isinstance(data, list):
        return result

    for item in data:
        if not isinstance(item, dict):
            continue

        name = (
            item.get("link2")
            or item.get("name")
            or item.get("title")
            or item.get("channelName")
            or ""
        )

        genre = (
            item.get("genre")
            or item.get("category")
            or ""
        )

        lang = (
            item.get("lang")
            or item.get("language")
            or ""
        )

        channel_id = (
            item.get("id")
            or item.get("channelId")
            or ""
        )

        logo = (
            item.get("img")
            or item.get("logo")
            or item.get("channelLogo")
            or ""
        )

        name = clean_text(name)

        if not name:
            continue

        result.append(
            {
                "name": name,
                "norm": normalize_name(name),
                "compact": compact_name(name),
                "genre": clean_text(genre),
                "lang": clean_text(lang),
                "id": clean_text(channel_id),
                "logo": clean_text(logo),
                "source": "jiotv",
            }
        )

    return result


def load_jiotv_reference():
    print("Fetching JioTV reference...")

    urls = [
        JIOTV_JSON_URL,
    ]

    for url in urls:
        try:
            raw = fetch_text(url)

            data = json.loads(raw)

            refs = parse_jiotv_json(data)

            if refs:
                print(f"  JioTV channels: {len(refs)}")
                return refs

        except Exception as exc:
            print(
                f"  JioTV JSON failed: "
                f"{type(exc).__name__}: {exc}"
            )

    print("  JioTV JSON unavailable.")

    return []


# ============================================================
# XMLTV REFERENCE
# ============================================================

def parse_xmltv(data, source_name):
    result = []

    try:
        if data[:2] == b"\x1f\x8b":
            data = gzip.decompress(data)

        root = ET.fromstring(data)

    except Exception as exc:
        print(
            f"  {source_name} XML error: "
            f"{type(exc).__name__}: {exc}"
        )
        return result

    for channel in root.findall(".//channel"):
        channel_id = clean_text(
            channel.attrib.get("id", "")
        )

        names = []

        for display in channel.findall("display-name"):
            text = clean_text(display.text or "")

            if text:
                names.append(text)

        if not names:
            continue

        name = names[0]

        result.append(
            {
                "name": name,
                "norm": normalize_name(name),
                "compact": compact_name(name),
                "genre": "",
                "lang": "",
                "id": channel_id,
                "logo": "",
                "source": source_name,
            }
        )

    return result


def load_epg_reference(url, source_name):
    try:
        data = fetch_bytes(url)

        refs = parse_xmltv(data, source_name)

        print(
            f"  {source_name} channels: {len(refs)}"
        )

        return refs

    except Exception as exc:
        print(
            f"  {source_name} reference failed: "
            f"{type(exc).__name__}: {exc}"
        )
        return []


# ============================================================
# REFERENCE INDEX
# ============================================================

def build_reference_index(refs):
    by_compact = {}
    by_norm = {}
    by_id = {}

    for ref in refs:
        compact = ref.get("compact", "")
        norm = ref.get("norm", "")
        rid = ref.get("id", "")

        if compact:
            by_compact.setdefault(
                compact,
                []
            ).append(ref)

        if norm:
            by_norm.setdefault(
                norm,
                []
            ).append(ref)

        if rid:
            by_id.setdefault(
                rid.lower(),
                []
            ).append(ref)

    return {
        "compact": by_compact,
        "norm": by_norm,
        "id": by_id,
        "all": refs,
    }


# ============================================================
# NAME MATCHING
# ============================================================

def source_tvg_id(entry):
    return (
        get_attr(entry, "tvg-id", "tvgid")
        .strip()
    )


def source_name(entry):
    attrs = entry.get("attrs", {})

    name = (
        get_attr(
            entry,
            "tvg-name",
            "channel-name",
        )
        or entry.get("name", "")
    )

    return clean_text(name)


def id_candidates(tvg_id):
    value = clean_text(tvg_id).lower()

    if not value:
        return []

    candidates = [value]

    if value.startswith("ts"):
        candidates.append(value[2:])

    if value.isdigit():
        candidates.append(value)

    return list(dict.fromkeys(candidates))


def exact_reference_match(entry, index):
    tvg_id = source_tvg_id(entry)
    name = source_name(entry)

    # --------------------------------------------------------
    # 1. Exact Jio/Tata ID match
    # --------------------------------------------------------

    for rid in id_candidates(tvg_id):
        matches = index["id"].get(rid, [])

        if matches:
            return matches[0], 100

    # --------------------------------------------------------
    # 2. Exact normalized name
    # --------------------------------------------------------

    compact = compact_name(name)

    if compact:
        matches = index["compact"].get(compact, [])

        if matches:
            return matches[0], 100

    norm = normalize_name(name)

    if norm:
        matches = index["norm"].get(norm, [])

        if matches:
            return matches[0], 100

    return None, 0


def fuzzy_reference_match(entry, index):
    name = source_name(entry)

    source_words = words(name)

    if not source_words:
        return None, 0

    compact = compact_name(name)

    best = None
    best_score = 0

    for ref in index["all"]:
        ref_words = words(ref.get("name", ""))

        if not ref_words:
            continue

        ref_compact = ref.get("compact", "")

        # One-token names are dangerous.
        # Don't fuzzy-match generic single words.
        if len(source_words) == 1 or len(ref_words) == 1:
            continue

        intersection = source_words & ref_words

        if not intersection:
            continue

        union = source_words | ref_words

        jaccard = (
            len(intersection) /
            max(1, len(union))
        )

        compact_bonus = 0

        if (
            compact
            and ref_compact
            and (
                compact in ref_compact
                or ref_compact in compact
            )
        ):
            compact_bonus = 0.35

        score = jaccard + compact_bonus

        # Strong overlap only.
        if score < 0.72:
            continue

        if score > best_score:
            best_score = score
            best = ref

    if best:
        return best, int(best_score * 100)

    return None, 0


# ============================================================
# LANGUAGE
# ============================================================

def normalize_language(value):
    value = clean_text(value).lower()

    if value in ALLOWED_LANGUAGES:
        return value

    if value.startswith("hindi"):
        return "hindi"

    if value.startswith("english"):
        return "english"

    if value.startswith("bhojpuri"):
        return "bhojpuri"

    return ""


def has_bad_language(value):
    value = clean_text(value).lower()

    for lang in BAD_LANGUAGES:
        if re.search(
            r"\b" + re.escape(lang) + r"\b",
            value,
        ):
            return True

    return False


def source_language(entry):
    return normalize_language(
        get_attr(
            entry,
            "tvg-language",
            "language",
            "lang",
        )
    )


# ============================================================
# GENRE MAPPING
# ============================================================

GENRE_MAP = {
    "news": "News",
    "entertainment": "Entertainment",
    "movies": "Movies",
    "movie": "Movies",
    "music": "Music",
    "kids": "Kids",
    "children": "Kids",
    "infotainment": "Infotainment",
    "science": "Science",
    "lifestyle": "Lifestyle",
    "business": "Business",
    "sports": "Sports",
    "sport": "Sports",
}


def map_genre(genre):
    value = normalize_name(genre)

    if not value:
        return ""

    if value in GENRE_MAP:
        return GENRE_MAP[value]

    for key, group in GENRE_MAP.items():
        if value == key:
            return group

    return ""


# ============================================================
# CURATED FALLBACK
#
# IMPORTANT:
# This NEVER decides whether a channel is Indian.
# It is only used AFTER the channel already matched JioTV/Tata.
# ============================================================

KNOWN_GENRE = {
    # NEWS
    "aaj tak": "News",
    "abp news": "News",
    "abp ananda": "News",
    "india today": "News",
    "news18 india": "News",
    "ndtv india": "News",
    "zee news": "News",
    "times now": "News",
    "times now navbharat": "News",
    "republic tv": "News",
    "republic bharat": "News",
    "cnn news18": "News",
    "news24": "News",

    # BUSINESS
    "cnbc tv18": "Business",
    "cnbc tv18 prime": "Business",
    "cnbc awaaz": "Business",
    "et now": "Business",
    "et now swadesh": "Business",
    "business today": "Business",

    # ENTERTAINMENT
    "colors": "Entertainment",
    "colors hd": "Entertainment",
    "sony sab": "Entertainment",
    "set": "Entertainment",
    "set hd": "Entertainment",
    "sony entertainment television": "Entertainment",
    "zee tv": "Entertainment",
    "and tv": "Entertainment",
    "star plus": "Entertainment",
    "star bharat": "Entertainment",
    "sony pal": "Entertainment",

    # MOVIES
    "zee cinema": "Movies",
    "zee cinema hd": "Movies",
    "sony max": "Movies",
    "sony max hd": "Movies",
    "star gold": "Movies",
    "star gold hd": "Movies",
    "b4u movies": "Movies",
    "bollywood 4u": "Movies",
    "shemaroo bollywood": "Movies",
    "and pictures": "Movies",
    "and pictures hd": "Movies",

    # MUSIC
    "b4u music": "Music",
    "9xm": "Music",
    "mtv": "Music",
    "mtv beats": "Music",
    "music india": "Music",
    "zoom": "Music",
    "9x jhakaas": "Music",

    # KIDS
    "cartoon network": "Kids",
    "pogo": "Kids",
    "nick": "Kids",
    "sonic": "Kids",
    "hungama": "Kids",
    "discovery kids": "Kids",

    # SCIENCE
    "discovery science": "Science",
    "history tv18": "Science",
    "history tv18 hd": "Science",
    "sony bbc earth": "Science",
    "national geographic": "Science",
    "nat geo": "Science",

    # LIFESTYLE
    "travelxp": "Lifestyle",
    "travel xp": "Lifestyle",
    "food food": "Lifestyle",
    "fashion tv": "Lifestyle",
    "tlc": "Lifestyle",

    # INFOTAINMENT
    "discovery": "Infotainment",
    "discovery hd": "Infotainment",
    "animal planet": "Infotainment",
    "epic": "Infotainment",

    # SPORTS
    "star sports": "Sports",
    "star sports 1": "Sports",
    "star sports 2": "Sports",
    "star sports select 1": "Sports",
    "star sports select 2": "Sports",
    "sony sports ten 1": "Sports",
    "sony sports ten 2": "Sports",
    "sony sports ten 3": "Sports",
    "sony sports ten 4": "Sports",
    "sony sports ten 5": "Sports",
    "dd sports": "Sports",
    "eurosport": "Sports",
    "jio cricket": "Sports",
}


def fallback_genre(ref):
    name = normalize_name(ref.get("name", ""))

    if not name:
        return ""

    if name in KNOWN_GENRE:
        return KNOWN_GENRE[name]

    compact = compact_name(name)

    for key, group in KNOWN_GENRE.items():
        if compact == compact_name(key):
            return group

    return ""


def classify_reference(ref):
    if not ref:
        return ""

    genre = map_genre(ref.get("genre", ""))

    if genre:
        return genre

    return fallback_genre(ref)


# ============================================================
# INDIAN LANGUAGE / CHANNEL FILTER
# ============================================================

def is_foreign_cricket(entry):
    name = source_name(entry).lower()

    if has_bad_language(name):
        return False

    return any(
        re.search(
            r"\b" + re.escape(word) + r"\b",
            name,
        )
        for word in FOREIGN_CRICKET_WORDS
    )


def resolve_channel(entry, index):
    name = source_name(entry)

    if not name:
        return None

    # --------------------------------------------------------
    # Explicitly reject obvious non-allowed language names
    # --------------------------------------------------------

    if has_bad_language(name):
        return None

    # --------------------------------------------------------
    # Exact match first
    # --------------------------------------------------------

    ref, score = exact_reference_match(
        entry,
        index,
    )

    # --------------------------------------------------------
    # Strong fuzzy match second
    # --------------------------------------------------------

    if ref is None:
        ref, score = fuzzy_reference_match(
            entry,
            index,
        )

    # --------------------------------------------------------
    # FOREIGN CRICKET EXCEPTION
    # --------------------------------------------------------

    if ref is None:
        if is_foreign_cricket(entry):
            return {
                "indian": False,
                "foreign_cricket": True,
                "ref": None,
                "group": "Sports",
                "language": "English",
                "score": 0,
            }

        return None

    # --------------------------------------------------------
    # Matched JioTV/Tata reference
    # --------------------------------------------------------

    ref_lang = normalize_language(
        ref.get("lang", "")
    )

    src_lang = source_language(entry)

    language = ref_lang or src_lang

    # If reference explicitly has a bad language, reject.
    ref_lang_raw = clean_text(
        ref.get("lang", "")
    ).lower()

    if ref_lang_raw and has_bad_language(ref_lang_raw):
        return None

    # Must have allowed language.
    if language not in ALLOWED_LANGUAGES:
        return None

    group = classify_reference(ref)

    if not group:
        return None

    if group not in GROUPS:
        return None

    return {
        "indian": True,
        "foreign_cricket": False,
        "ref": ref,
        "group": group,
        "language": language.title(),
        "score": score,
    }


# ============================================================
# OUTPUT
# ============================================================

def escape_m3u(value):
    value = clean_text(value)

    return value.replace('"', "'")


def build_extinf(entry, resolved):
    ref = resolved.get("ref")

    group = resolved["group"]
    language = resolved["language"]

    name = source_name(entry)

    logo = get_attr(
        entry,
        "tvg-logo",
        "logo",
    )

    tvg_id = source_tvg_id(entry)

    # Prefer reference logo if source has none.
    if not logo and ref:
        logo = ref.get("logo", "")

    # Prefer canonical reference name only when
    # it is safe and useful.
    if ref:
        ref_name = clean_text(
            ref.get("name", "")
        )

        if ref_name:
            # Keep source display name when it is
            # more descriptive, otherwise reference.
            if len(ref_name) >= 3:
                name = ref_name

    attrs = []

    if tvg_id:
        attrs.append(
            f'tvg-id="{escape_m3u(tvg_id)}"'
        )
    elif ref:
        rid = clean_text(ref.get("id", ""))

        if rid:
            attrs.append(
                f'tvg-id="{escape_m3u(rid)}"'
            )

    if logo:
        attrs.append(
            f'tvg-logo="{escape_m3u(logo)}"'
        )

    attrs.append(
        f'group-title="{escape_m3u(group)}"'
    )

    attrs.append(
        f'tvg-language="{escape_m3u(language)}"'
    )

    return (
        "#EXTINF:-1 "
        + " ".join(attrs)
        + ","
        + escape_m3u(name)
    )


# ============================================================
# URL NORMALIZATION
# ============================================================

def normalize_url(url):
    url = clean_text(url)

    # Exact URL means exact after trimming.
    # Do not remove query parameters because different
    # query URLs can be different streams.
    return url


def url_key(url):
    return normalize_url(url)


# ============================================================
# SOURCE LOADING
# ============================================================

def load_sources(source_dir):
    entries = []

    source_path = Path(source_dir)

    if source_path.exists():
        files = sorted(
            p for p in source_path.rglob("*")
            if p.is_file()
            and p.suffix.lower() in {
                ".m3u",
                ".m3u8",
                ".txt",
            }
        )

        for path in files:
            try:
                text = path.read_text(
                    encoding="utf-8",
                    errors="replace",
                )

                parsed = parse_m3u(text)

                print(
                    f"  {path}: "
                    f"{len(parsed)} entries"
                )

                entries.extend(parsed)

            except Exception as exc:
                print(
                    f"  Failed {path}: "
                    f"{type(exc).__name__}: {exc}"
                )

        if entries:
            return entries

    print("Fetching source playlists...")

    for url in SOURCE_URLS:
        try:
            text = fetch_text(url)

            parsed = parse_m3u(text)

            print(
                f"  {url.rsplit('/', 1)[-1]}: "
                f"{len(parsed)} entries"
            )

            entries.extend(parsed)

        except Exception as exc:
            print(
                f"  Source failed {url}: "
                f"{type(exc).__name__}: {exc}"
            )

    return entries


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Build grouped Indian IPTV playlist "
            "using JioTV/Tata Play references."
        )
    )

    parser.add_argument(
        "sources",
        nargs="?",
        default="sources",
        help="Source directory",
    )

    parser.add_argument(
        "-o",
        "--output",
        default="playlist.m3u",
        help="Output M3U file",
    )

    args = parser.parse_args()

    # --------------------------------------------------------
    # References
    # --------------------------------------------------------

    jio_refs = load_jiotv_reference()

    tata_refs = load_epg_reference(
        TATAPLAY_EPG_URL,
        "Tata Play",
    )

    # We do not use Tata EPG genre because XMLTV channel
    # records do not reliably contain genre/language.
    # Tata is used as a channel identity reference.

    all_refs = []

    all_refs.extend(jio_refs)
    all_refs.extend(tata_refs)

    index = build_reference_index(
        all_refs
    )

    print(
        f"  Total reference names: "
        f"{len(all_refs)}"
    )

    # --------------------------------------------------------
    # Sources
    # --------------------------------------------------------

    source_entries = load_sources(
        args.sources
    )

    print(
        f"Total source entries: "
        f"{len(source_entries)}"
    )

    # --------------------------------------------------------
    # First resolve everything.
    #
    # Indian matches get priority over foreign-cricket
    # exception when the exact same URL appears twice.
    # --------------------------------------------------------

    resolved_entries = []

    stats = {
        "source": len(source_entries),
        "indian": 0,
        "foreign_cricket": 0,
        "rejected": 0,
    }

    for entry in source_entries:
        url = normalize_url(
            entry.get("url", "")
        )

        if not url:
            stats["rejected"] += 1
            continue

        result = resolve_channel(
            entry,
            index,
        )

        if result is None:
            stats["rejected"] += 1
            continue

        if result["indian"]:
            stats["indian"] += 1
            priority = 0
        else:
            stats["foreign_cricket"] += 1
            priority = 1

        resolved_entries.append(
            (
                priority,
                entry,
                result,
            )
        )

    # --------------------------------------------------------
    # Indian first.
    # --------------------------------------------------------

    resolved_entries.sort(
        key=lambda item: item[0]
    )

    # --------------------------------------------------------
    # Global exact URL dedup.
    #
    # Same URL under different channel names:
    # only one entry.
    #
    # Same channel with different URLs:
    # all retained.
    # --------------------------------------------------------

    seen_urls = set()

    final_entries = []

    for priority, entry, result in resolved_entries:
        url = normalize_url(
            entry.get("url", "")
        )

        key = url_key(url)

        if not key:
            continue

        if key in seen_urls:
            continue

        seen_urls.add(key)

        final_entries.append(
            (
                entry,
                result,
                url,
            )
        )

    # --------------------------------------------------------
    # Group
    # --------------------------------------------------------

    grouped = {
        group: []
        for group in GROUPS
    }

    for entry, result, url in final_entries:
        group = result["group"]

        if group not in grouped:
            continue

        grouped[group].append(
            (
                entry,
                result,
                url,
            )
        )

    # --------------------------------------------------------
    # Stable sorting inside groups.
    # --------------------------------------------------------

    for group in GROUPS:
        grouped[group].sort(
            key=lambda item: (
                normalize_name(
                    source_name(item[0])
                ),
                item[2],
            )
        )

    # --------------------------------------------------------
    # Write
    # --------------------------------------------------------

    output = Path(args.output)

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    lines = [
        "#EXTM3U",
        (
            '#EXTVLCOPT:http-referrer=""'
        ),
    ]

    total = 0

    for group in GROUPS:
        items = grouped[group]

        if not items:
            continue

        for entry, result, url in items:
            lines.append(
                build_extinf(
                    entry,
                    result,
                )
            )

            lines.append(url)

            total += 1

    output.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # Report
    # --------------------------------------------------------

    print()
    print("========================================")
    print("PLAYLIST COMPLETE")
    print("========================================")
    print(
        f"Source entries       : {stats['source']}"
    )
    print(
        f"Indian matched       : {stats['indian']}"
    )
    print(
        f"Foreign cricket      : {stats['foreign_cricket']}"
    )
    print(
        f"Rejected              : {stats['rejected']}"
    )
    print(
        f"Final unique streams  : {total}"
    )
    print(
        f"Output                : {output}"
    )
    print()

    for group in GROUPS:
        print(
            f"{group:15} : "
            f"{len(grouped[group])}"
        )


if __name__ == "__main__":
    main()
