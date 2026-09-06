#!/usr/bin/env python3

import argparse
import gzip
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from difflib import SequenceMatcher


SOURCE_URLS = [
    "https://raw.githubusercontent.com/wizakorhd/iptv/main/playlist-hindi.m3u",
    "https://raw.githubusercontent.com/wizakorhd/iptv/main/playlist-english-india.m3u",
    "https://raw.githubusercontent.com/wizakorhd/iptv/main/playlist-top.m3u",
    "https://raw.githubusercontent.com/wizakorhd/iptv/main/playlist.m3u",
]

JIOTV_JSON_URL = (
    "https://gist.githubusercontent.com/mitthu786/"
    "a6e246c3f0012cdd85a7e5fc3128348f/raw/tsjiotv.json"
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

BAD_LANGUAGES = {
    "bengali", "bangla", "tamil", "telugu", "kannada",
    "malayalam", "marathi", "punjabi", "gujarati",
    "odia", "oriya", "assamese", "nepali", "urdu",
    "sinhala", "konkani", "manipuri", "meitei",
    "sindhi", "kashmiri", "dogri", "maithili",
    "rajasthani", "haryanvi", "chhattisgarhi",
}

FOREIGN_CRICKET_WORDS = (
    "cricket",
    "icc",
)

# Foreign sports exceptions.
# These are allowed in Sports even without JioTV/Tata Play matching.
SPECIAL_FOREIGN_SPORTS_PATTERNS = (
    r"\bsky\s*sports\b",
    r"\bwillow\b",
)

GENRE_MAP = {
    "news": "News",

    "entertainment": "Entertainment",

    "movie": "Movies",
    "movies": "Movies",
    "film": "Movies",
    "films": "Movies",

    "music": "Music",

    "kids": "Kids",
    "children": "Kids",

    "infotainment": "Infotainment",
    "documentary": "Infotainment",
    "documentaries": "Infotainment",
    "general": "Infotainment",
    "special interest": "Infotainment",
    "travel": "Infotainment",

    "science": "Science",
    "technology": "Science",
    "technology science": "Science",

    "lifestyle": "Lifestyle",
    "lifestyle leisure": "Lifestyle",

    "business": "Business",
    "business news": "Business",

    "sports": "Sports",
    "sport": "Sports",
}


def fetch_bytes(url, timeout=60):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/140.0 Safari/537.36"
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
            continue

    return data.decode("utf-8", errors="replace")


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

    value = value.replace("ᶠᴴᴰ", " ")
    value = value.replace("ᴴᴰ", " ")

    value = re.sub(r"\s+", " ", value)

    return value.strip()


def normalize_name(value):
    value = clean_text(value).lower()

    value = value.replace("_", " ")
    value = value.replace("&", " and ")

    value = re.sub(
        r"\b(?:uhd|4k|8k|fhd|hd|sd|hevc|h265|h264|"
        r"1080p|720p|576p|480p)\b",
        " ",
        value,
    )

    value = re.sub(
        r"\b(?:hindi|english|bhojpuri)\b",
        " ",
        value,
    )

    value = re.sub(
        r"\b(?:india|indian)\b",
        " ",
        value,
    )

    value = re.sub(r"[^a-z0-9]+", " ", value)
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def compact_name(value):
    return re.sub(
        r"[^a-z0-9]+",
        "",
        normalize_name(value),
    )


def identity_tokens(value):
    generic = {
        "tv",
        "television",
        "channel",
        "live",
        "network",
        "india",
        "indian",
    }

    return {
        x
        for x in normalize_name(value).split()
        if x not in generic
    }


def parse_attrs(line):
    attrs = {}

    for match in re.finditer(
        r'([\w-]+)="([^"]*)"',
        line,
    ):
        attrs[match.group(1)] = match.group(2)

    return attrs


def parse_m3u(text):
    entries = []
    current = None
    pending_options = []

    for raw in text.splitlines():
        line = raw.strip()

        if not line:
            continue

        if line.startswith("#EXTVLCOPT:"):
            if current is not None:
                current.setdefault("options", []).append(line)
            else:
                pending_options.append(line)
            continue

        if line.startswith("#EXTINF:"):
            current = {
                "extinf": line,
                "url": "",
                "name": "",
                "attrs": parse_attrs(line),
                "options": list(pending_options),
            }

            pending_options = []

            comma = line.find(",")

            if comma >= 0:
                current["name"] = clean_text(
                    line[comma + 1:]
                )

            continue

        if (
            not line.startswith("#")
            and current is not None
        ):
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


def source_name(entry):
    return (
        clean_text(entry.get("name", ""))
        or get_attr(
            entry,
            "tvg-name",
            "channel-name",
            "name",
        )
    )


def source_tvg_id(entry):
    return get_attr(
        entry,
        "tvg-id",
        "tvgid",
    )


def parse_jiotv_json(data):
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
        return []

    result = []

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

        if not name:
            continue

        result.append({
            "name": clean_text(name),
            "norm": normalize_name(name),
            "compact": compact_name(name),
            "tokens": identity_tokens(name),
            "genre": clean_text(
                item.get("genre")
                or item.get("category")
                or ""
            ),
            "lang": clean_text(
                item.get("lang")
                or item.get("language")
                or ""
            ),
            "id": clean_text(
                item.get("id")
                or item.get("channelId")
                or ""
            ),
            "logo": clean_text(
                item.get("img")
                or item.get("logo")
                or item.get("channelLogo")
                or ""
            ),
            "source": "jiotv",
        })

    return result


def load_jiotv_reference():
    print("Fetching JioTV reference...")

    try:
        raw = fetch_text(JIOTV_JSON_URL)
        refs = parse_jiotv_json(json.loads(raw))

        print(f"  JioTV channels: {len(refs)}")

        return refs

    except Exception as exc:
        print(
            "  JioTV reference failed: "
            f"{type(exc).__name__}: {exc}"
        )
        return []


def xml_text(element):
    if element is None:
        return ""

    return clean_text(
        "".join(element.itertext())
    )


def parse_xmltv(data, source_name_value):
    try:
        if data[:2] == b"\x1f\x8b":
            data = gzip.decompress(data)

        root = ET.fromstring(data)

    except Exception as exc:
        print(
            f"  {source_name_value} XML error: "
            f"{type(exc).__name__}: {exc}"
        )
        return []

    channels = {}

    for channel in root.findall(".//channel"):
        cid = clean_text(
            channel.attrib.get("id", "")
        )

        if not cid:
            continue

        names = []

        for display in channel.findall("display-name"):
            text = xml_text(display)

            if text and text not in names:
                names.append(text)

        if not names:
            continue

        channels[cid] = {
            "names": names,
            "categories": [],
            "languages": [],
        }

    for program in root.findall(".//programme"):
        cid = clean_text(
            program.attrib.get("channel", "")
        )

        if cid not in channels:
            continue

        for category in program.findall("category"):
            value = xml_text(category)

            if value:
                channels[cid]["categories"].append(value)

        for language in program.findall("language"):
            value = xml_text(language)

            if value:
                channels[cid]["languages"].append(value)

    result = []

    for cid, data_item in channels.items():
        categories = data_item["categories"]
        languages = data_item["languages"]

        genre = ""

        if categories:
            counts = {}

            for category in categories:
                mapped = map_genre(category)

                if mapped:
                    counts[mapped] = (
                        counts.get(mapped, 0) + 1
                    )

            if counts:
                genre = max(
                    counts,
                    key=counts.get,
                )

        lang = ""

        if languages:
            lang_counts = {}

            for language in languages:
                normalized = normalize_language(
                    language
                )

                if normalized:
                    lang_counts[normalized] = (
                        lang_counts.get(
                            normalized,
                            0,
                        ) + 1
                    )

            if lang_counts:
                lang = max(
                    lang_counts,
                    key=lang_counts.get,
                )

        for name in data_item["names"]:
            result.append({
                "name": name,
                "norm": normalize_name(name),
                "compact": compact_name(name),
                "tokens": identity_tokens(name),
                "genre": genre,
                "lang": lang,
                "id": cid,
                "logo": "",
                "source": source_name_value,
            })

    return result


def load_epg_reference(url, source_name_value):
    try:
        data = fetch_bytes(url)

        refs = parse_xmltv(
            data,
            source_name_value,
        )

        print(
            f"  {source_name_value} channels: "
            f"{len(refs)}"
        )

        return refs

    except Exception as exc:
        print(
            f"  {source_name_value} reference failed: "
            f"{type(exc).__name__}: {exc}"
        )
        return []


def build_reference_index(refs):
    index = {
        "compact": {},
        "norm": {},
        "id": {},
        "all": refs,
    }

    for ref in refs:
        if ref.get("compact"):
            index["compact"].setdefault(
                ref["compact"],
                [],
            ).append(ref)

        if ref.get("norm"):
            index["norm"].setdefault(
                ref["norm"],
                [],
            ).append(ref)

        rid = clean_text(
            ref.get("id", "")
        ).lower()

        if rid:
            index["id"].setdefault(
                rid,
                [],
            ).append(ref)

    return index


def normalize_language(value):
    value = clean_text(value).lower()

    if not value:
        return ""

    found = []

    for language in ALLOWED_LANGUAGES:
        if re.search(
            r"\b"
            + re.escape(language)
            + r"\b",
            value,
        ):
            found.append(language)

    if "hindi" in found:
        return "hindi"

    if "english" in found:
        return "english"

    if "bhojpuri" in found:
        return "bhojpuri"

    return ""


def has_bad_language(value):
    value = clean_text(value).lower()

    return any(
        re.search(
            r"\b"
            + re.escape(language)
            + r"\b",
            value,
        )
        for language in BAD_LANGUAGES
    )


def source_language(entry):
    return normalize_language(
        get_attr(
            entry,
            "tvg-language",
            "language",
            "lang",
        )
    )


def map_genre(value):
    value = normalize_name(value)

    if not value:
        return ""

    direct = GENRE_MAP.get(value)

    if direct:
        return direct

    for key, group in GENRE_MAP.items():
        if key in value:
            return group

    return ""


def id_candidates(value):
    value = clean_text(value).lower()

    if not value:
        return []

    result = [value]

    if value.startswith("ts"):
        result.append(value[2:])

    return list(dict.fromkeys(result))


def choose_reference(refs):
    if not refs:
        return None

    for ref in refs:
        if ref.get("source") == "jiotv":
            return ref

    return refs[0]


def exact_match(entry, index):
    tvg_id = source_tvg_id(entry)
    name = source_name(entry)

    for rid in id_candidates(tvg_id):
        found = index["id"].get(rid, [])

        if found:
            return choose_reference(found), 100

    compact = compact_name(name)

    if compact:
        found = index["compact"].get(
            compact,
            [],
        )

        if found:
            return choose_reference(found), 100

    norm = normalize_name(name)

    if norm:
        found = index["norm"].get(
            norm,
            [],
        )

        if found:
            return choose_reference(found), 100

    return None, 0


def similarity_score(source, reference):
    source_compact = compact_name(source)
    reference_compact = compact_name(reference)

    if not source_compact or not reference_compact:
        return 0.0

    source_tokens = identity_tokens(source)
    reference_tokens = identity_tokens(reference)

    if not source_tokens or not reference_tokens:
        return 0.0

    common = source_tokens & reference_tokens

    if not common:
        return 0.0

    union = source_tokens | reference_tokens
    jaccard = len(common) / len(union)

    sequence = SequenceMatcher(
        None,
        source_compact,
        reference_compact,
    ).ratio()

    containment = 0.0

    if (
        len(source_compact) >= 5
        and (
            source_compact in reference_compact
            or reference_compact in source_compact
        )
    ):
        containment = 0.20

    score = (
        (jaccard * 0.55)
        + (sequence * 0.45)
        + containment
    )

    return min(score, 1.0)


def fuzzy_match(entry, index):
    source = source_name(entry)

    if not source:
        return None, 0

    best_ref = None
    best_score = 0.0

    for ref in index["all"]:
        score = similarity_score(
            source,
            ref.get("name", ""),
        )

        if score < 0.72:
            continue

        if (
            score > best_score
            or (
                score == best_score
                and best_ref is not None
                and ref.get("source") == "jiotv"
                and best_ref.get("source") != "jiotv"
            )
        ):
            best_score = score
            best_ref = ref

    if best_ref is None:
        return None, 0

    return (
        best_ref,
        int(best_score * 100),
    )


def is_foreign_cricket(entry):
    name = source_name(entry).lower()

    if has_bad_language(name):
        return False

    return any(
        re.search(
            r"\b"
            + re.escape(word)
            + r"\b",
            name,
        )
        for word in FOREIGN_CRICKET_WORDS
    )


def is_special_foreign_sports(entry):
    name = source_name(entry).lower()

    if not name:
        return False

    if has_bad_language(name):
        return False

    return any(
        re.search(
            pattern,
            name,
            re.IGNORECASE,
        )
        for pattern in SPECIAL_FOREIGN_SPORTS_PATTERNS
    )


def resolve_channel(entry, index):
    name = source_name(entry)

    if not name:
        return None

    # Sky Sports + all Willow variants.
    # These are explicitly allowed as foreign Sports channels.
    if is_special_foreign_sports(entry):
        return {
            "indian": False,
            "group": "Sports",
            "language": "English",
            "ref": None,
            "score": 0,
        }

    if has_bad_language(name):
        return None

    ref, score = exact_match(
        entry,
        index,
    )

    if ref is None:
        ref, score = fuzzy_match(
            entry,
            index,
        )

    if ref is None:
        if is_foreign_cricket(entry):
            return {
                "indian": False,
                "group": "Sports",
                "language": "English",
                "ref": None,
                "score": 0,
            }

        return None

    ref_lang = normalize_language(
        ref.get("lang", "")
    )

    if ref.get("lang") and has_bad_language(
        ref.get("lang")
    ):
        return None

    language = (
        ref_lang
        or source_language(entry)
    )

    if language not in ALLOWED_LANGUAGES:
        return None

    group = map_genre(
        ref.get("genre", "")
    )

    if group not in GROUPS:
        return None

    return {
        "indian": True,
        "group": group,
        "language": language.title(),
        "ref": ref,
        "score": score,
    }


def escape_m3u(value):
    return clean_text(value).replace(
        '"',
        "'",
    )


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

    if not logo and ref:
        logo = ref.get("logo", "")

    attrs = []

    if tvg_id:
        attrs.append(
            f'tvg-id="{escape_m3u(tvg_id)}"'
        )
    elif ref and ref.get("id"):
        attrs.append(
            f'tvg-id="{escape_m3u(ref["id"])}"'
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


def normalize_url(url):
    return clean_text(url)


def url_key(url):
    return normalize_url(url).lower()


def load_sources():
    """
    ONLY the four configured WizakorHD playlists.
    No arbitrary local source files are loaded.
    """

    entries = []

    print("Fetching WizakorHD source playlists...")

    for url in SOURCE_URLS:
        filename = url.rsplit("/", 1)[-1]

        try:
            text = fetch_text(url)
            parsed = parse_m3u(text)

            print(
                f"  {filename}: "
                f"{len(parsed)} entries"
            )

            entries.extend(parsed)

        except Exception as exc:
            print(
                f"  {filename} failed: "
                f"{type(exc).__name__}: {exc}"
            )

    return entries


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "sources",
        nargs="?",
        default="sources",
    )

    parser.add_argument(
        "-o",
        "--output",
        default="playlist.m3u",
    )

    args = parser.parse_args()

    print("========================================")
    print("Loading references")
    print("========================================")

    jio_refs = load_jiotv_reference()

    tata_refs = load_epg_reference(
        TATAPLAY_EPG_URL,
        "Tata Play",
    )

    # JioTV preferred; Tata Play supplements identity.
    all_refs = jio_refs + tata_refs

    index = build_reference_index(
        all_refs
    )

    print(
        f"  Total reference names: "
        f"{len(all_refs)}"
    )

    print()
    print("========================================")
    print("Loading streams")
    print("========================================")

    source_entries = load_sources()

    print(
        f"Total source entries: "
        f"{len(source_entries)}"
    )

    stats = {
        "source": len(source_entries),
        "indian": 0,
        "foreign_cricket": 0,
        "foreign_special_sports": 0,
        "rejected": 0,
    }

    resolved = []

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

        elif is_special_foreign_sports(entry):
            stats["foreign_special_sports"] += 1
            priority = 1

        else:
            stats["foreign_cricket"] += 1
            priority = 2

        resolved.append(
            (
                priority,
                entry,
                result,
                url,
            )
        )

    # Indian first, special foreign sports next,
    # foreign cricket after that.
    resolved.sort(
        key=lambda item: (
            item[0],
            normalize_name(
                source_name(item[1])
            ),
            item[3].lower(),
        )
    )

    # Global exact URL dedup.
    # Same channel + different URLs remain.
    seen_urls = set()
    final_entries = []

    for _, entry, result, url in resolved:
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

    grouped = {
        group: []
        for group in GROUPS
    }

    for entry, result, url in final_entries:
        group = result["group"]

        if group in grouped:
            grouped[group].append(
                (
                    entry,
                    result,
                    url,
                )
            )

    for group in GROUPS:
        grouped[group].sort(
            key=lambda item: (
                normalize_name(
                    source_name(item[0])
                ),
                item[2].lower(),
            )
        )

    output = Path(args.output)

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    lines = ["#EXTM3U"]

    total = 0

    for group in GROUPS:
        for entry, result, url in grouped[group]:
            lines.append(
                build_extinf(
                    entry,
                    result,
                )
            )

            # Preserve Wizakor VLC options such as
            # http-user-agent / http-referrer.
            for option in entry.get(
                "options",
                [],
            ):
                lines.append(option)

            lines.append(url)

            total += 1

    output.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print()
    print("========================================")
    print("PLAYLIST COMPLETE")
    print("========================================")
    print(
        f"Source entries          : "
        f"{stats['source']}"
    )
    print(
        f"Indian matched          : "
        f"{stats['indian']}"
    )
    print(
        f"Foreign special Sports : "
        f"{stats['foreign_special_sports']}"
    )
    print(
        f"Foreign cricket         : "
        f"{stats['foreign_cricket']}"
    )
    print(
        f"Rejected                : "
        f"{stats['rejected']}"
    )
    print(
        f"Final unique streams    : "
        f"{total}"
    )
    print(
        f"Output                  : "
        f"{output}"
    )
    print()

    for group in GROUPS:
        print(
            f"{group:15} : "
            f"{len(grouped[group])}"
        )


if __name__ == "__main__":
    main()
