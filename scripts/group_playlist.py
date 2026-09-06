```python
#!/usr/bin/env python3

import argparse
import gzip
import json
import re
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path


# ============================================================
# CONFIG
# ============================================================

SOURCE_URLS = [
    "https://raw.githubusercontent.com/wizakorhd/iptv/main/playlist-hindi.m3u",
    "https://raw.githubusercontent.com/wizakorhd/iptv/main/playlist-english-india.m3u",
    "https://raw.githubusercontent.com/wizakorhd/iptv/main/playlist-top.m3u",
    "https://raw.githubusercontent.com/wizakorhd/iptv/main/playlist.m3u",
]

# Correct mitthu786 gist
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

FOREIGN_CRICKET_WORDS = (
    "cricket",
    "icc",
)


# ============================================================
# HTTP
# ============================================================

def fetch_bytes(url, timeout=45):
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
# TEXT / NORMALIZATION
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


def normalize_name(value):
    value = clean_text(value).lower()

    # Unicode HD/FHD decorations
    value = value.replace("ᶠᴴᴰ", " ")
    value = value.replace("ᴴᴰ", " ")
    value = value.replace("ᶠᴴᴰ", " ")

    # Common separators
    value = value.replace("_", " ")
    value = value.replace("&", " and ")

    # Remove quality markers
    value = re.sub(
        r"\b("
        r"uhd|4k|8k|fhd|hd|sd|"
        r"hevc|h265|h264|"
        r"1080p|720p|576p|480p"
        r")\b",
        " ",
        value,
        flags=re.I,
    )

    # Remove common feed suffixes
    value = re.sub(
        r"\b("
        r"live|channel|tv|television"
        r")\b$",
        "",
        value,
        flags=re.I,
    )

    # Remove India marker only when used as suffix/prefix
    value = re.sub(
        r"\b(india|indian)\b",
        " ",
        value,
        flags=re.I,
    )

    # Remove language suffixes from identity comparison.
    # Language itself is checked separately.
    value = re.sub(
        r"\b("
        r"hindi|english|bhojpuri"
        r")\b",
        " ",
        value,
        flags=re.I,
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


def compact_name(value):
    return re.sub(
        r"[^a-z0-9]+",
        "",
        normalize_name(value),
    )


def words(value):
    return set(
        normalize_name(value).split()
    )


# ============================================================
# M3U
# ============================================================

def parse_m3u(text):
    entries = []

    current = None

    for raw in text.splitlines():
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
                current["name"] = clean_text(
                    line[comma + 1:]
                )

            attrs_part = (
                line[:comma]
                if comma >= 0
                else line
            )

            for match in re.finditer(
                r'([\w-]+)="([^"]*)"',
                attrs_part,
            ):
                current["attrs"][
                    match.group(1)
                ] = match.group(2)

        elif (
            not line.startswith("#")
            and current is not None
        ):
            current["url"] = line

            if current["url"]:
                entries.append(current)

            current = None

    return entries


def get_attr(entry, *names):
    attrs = entry.get(
        "attrs",
        {},
    )

    for name in names:
        value = attrs.get(name)

        if value:
            return clean_text(value)

    return ""


def source_name(entry):
    # IMPORTANT:
    # Display name from EXTINF is the most reliable
    # Wizakor channel name.
    display_name = clean_text(
        entry.get("name", "")
    )

    if display_name:
        return display_name

    return (
        get_attr(
            entry,
            "tvg-name",
            "channel-name",
            "name",
        )
        or ""
    )


def source_tvg_id(entry):
    return get_attr(
        entry,
        "tvg-id",
        "tvgid",
    )


# ============================================================
# JIOTV JSON
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
            if isinstance(
                data.get(key),
                list,
            ):
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

        result.append({
            "name": name,
            "norm": normalize_name(name),
            "compact": compact_name(name),
            "genre": clean_text(genre),
            "lang": clean_text(lang),
            "id": clean_text(channel_id),
            "logo": clean_text(logo),
            "source": "jiotv",
        })

    return result


def load_jiotv_reference():
    print("Fetching JioTV reference...")

    try:
        raw = fetch_text(
            JIOTV_JSON_URL
        )

        data = json.loads(raw)

        refs = parse_jiotv_json(data)

        if refs:
            print(
                f"  JioTV channels: {len(refs)}"
            )
            return refs

    except Exception as exc:
        print(
            "  JioTV JSON failed: "
            f"{type(exc).__name__}: {exc}"
        )

    print("  JioTV JSON unavailable.")

    return []


# ============================================================
# XMLTV
# ============================================================

def parse_xmltv(data, source_name_value):
    result = []

    try:
        if data[:2] == b"\x1f\x8b":
            data = gzip.decompress(data)

        root = ET.fromstring(data)

    except Exception as exc:
        print(
            f"  {source_name_value} XML error: "
            f"{type(exc).__name__}: {exc}"
        )
        return result

    for channel in root.findall(
        ".//channel"
    ):
        channel_id = clean_text(
            channel.attrib.get(
                "id",
                "",
            )
        )

        names = []

        for display in channel.findall(
            "display-name"
        ):
            text = clean_text(
                display.text or ""
            )

            if text:
                names.append(text)

        if not names:
            continue

        for name in names:
            result.append({
                "name": name,
                "norm": normalize_name(name),
                "compact": compact_name(name),
                "genre": "",
                "lang": "",
                "id": channel_id,
                "logo": "",
                "source": source_name_value,
            })

    return result


def load_epg_reference(
    url,
    source_name_value,
):
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


# ============================================================
# REFERENCE INDEX
# ============================================================

def build_reference_index(refs):
    by_compact = {}
    by_norm = {}
    by_id = {}

    for ref in refs:
        compact = ref.get(
            "compact",
            "",
        )

        norm = ref.get(
            "norm",
            "",
        )

        rid = clean_text(
            ref.get(
                "id",
                "",
            )
        ).lower()

        if compact:
            by_compact.setdefault(
                compact,
                [],
            ).append(ref)

        if norm:
            by_norm.setdefault(
                norm,
                [],
            ).append(ref)

        if rid:
            by_id.setdefault(
                rid,
                [],
            ).append(ref)

    return {
        "compact": by_compact,
        "norm": by_norm,
        "id": by_id,
        "all": refs,
    }


# ============================================================
# LANGUAGE
# ============================================================

def normalize_language(value):
    value = clean_text(
        value
    ).lower()

    if not value:
        return ""

    # Handle values such as:
    # "Hindi / English"
    # "English,Hindi"
    # "Hindi English"
    found = []

    for lang in ALLOWED_LANGUAGES:
        if re.search(
            r"\b"
            + re.escape(lang)
            + r"\b",
            value,
        ):
            found.append(lang)

    if len(found) == 1:
        return found[0]

    # Prefer Hindi if multiple allowed languages
    if "hindi" in found:
        return "hindi"

    if "english" in found:
        return "english"

    if "bhojpuri" in found:
        return "bhojpuri"

    return ""


def has_bad_language(value):
    value = clean_text(
        value
    ).lower()

    for lang in BAD_LANGUAGES:
        if re.search(
            r"\b"
            + re.escape(lang)
            + r"\b",
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
# GENRE
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


def map_genre(value):
    value = normalize_name(
        value
    )

    if not value:
        return ""

    return GENRE_MAP.get(
        value,
        "",
    )


# ============================================================
# MATCHING HELPERS
# ============================================================

def id_candidates(value):
    value = clean_text(
        value
    ).lower()

    if not value:
        return []

    candidates = [
        value
    ]

    if value.startswith("ts"):
        candidates.append(
            value[2:]
        )

    return list(
        dict.fromkeys(
            candidates
        )
    )


def choose_jio(refs):
    """
    Prefer JioTV over Tata EPG because Jio reference
    contains genre + language.
    """
    for ref in refs:
        if ref.get("source") == "jiotv":
            return ref

    return refs[0] if refs else None


def exact_match(entry, index):
    tvg_id = source_tvg_id(
        entry
    )

    name = source_name(
        entry
    )

    # 1. Exact ID
    for rid in id_candidates(
        tvg_id
    ):
        matches = index["id"].get(
            rid,
            [],
        )

        if matches:
            ref = choose_jio(
                matches
            )

            return ref, 100

    # 2. Exact compact name
    compact = compact_name(
        name
    )

    if compact:
        matches = index[
            "compact"
        ].get(
            compact,
            [],
        )

        if matches:
            ref = choose_jio(
                matches
            )

            return ref, 100

    # 3. Exact normalized name
    norm = normalize_name(
        name
    )

    if norm:
        matches = index[
            "norm"
        ].get(
            norm,
            [],
        )

        if matches:
            ref = choose_jio(
                matches
            )

            return ref, 100

    return None, 0


def fuzzy_match(entry, index):
    name = source_name(
        entry
    )

    src_words = words(
        name
    )

    if not src_words:
        return None, 0

    src_compact = compact_name(
        name
    )

    best = None
    best_score = 0.0

    for ref in index["all"]:
        ref_name = ref.get(
            "name",
            "",
        )

        ref_words = words(
            ref_name
        )

        if not ref_words:
            continue

        # Avoid dangerous one-word fuzzy matches.
        if (
            len(src_words) == 1
            or len(ref_words) == 1
        ):
            continue

        intersection = (
            src_words & ref_words
        )

        if not intersection:
            continue

        union = (
            src_words | ref_words
        )

        jaccard = (
            len(intersection)
            / max(1, len(union))
        )

        ref_compact = ref.get(
            "compact",
            "",
        )

        bonus = 0.0

        if (
            src_compact
            and ref_compact
            and (
                src_compact
                in ref_compact
                or ref_compact
                in src_compact
            )
        ):
            bonus = 0.30

        # First-word / brand overlap bonus
        src_first = next(
            iter(src_words),
            "",
        )

        if src_first in ref_words:
            bonus += 0.05

        score = (
            jaccard
            + bonus
        )

        if score < 0.70:
            continue

        # Jio preferred
        if (
            score == best_score
            and best is not None
            and ref.get("source")
            == "jiotv"
        ):
            best = ref
            continue

        if score > best_score:
            best_score = score
            best = ref

    if best is None:
        return None, 0

    return (
        best,
        int(best_score * 100),
    )


# ============================================================
# FOREIGN CRICKET
# ============================================================

def is_foreign_cricket(entry):
    name = source_name(
        entry
    ).lower()

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


# ============================================================
# RESOLVE
# ============================================================

def resolve_channel(
    entry,
    index,
):
    name = source_name(
        entry
    )

    if not name:
        return None

    # Explicit bad-language channel name
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

    # Foreign cricket exception
    if ref is None:
        if is_foreign_cricket(
            entry
        ):
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
    # Language
    # --------------------------------------------------------

    ref_lang_raw = clean_text(
        ref.get(
            "lang",
            "",
        )
    )

    if ref_lang_raw and has_bad_language(
        ref_lang_raw
    ):
        return None

    ref_lang = normalize_language(
        ref_lang_raw
    )

    src_lang = source_language(
        entry
    )

    language = (
        ref_lang
        or src_lang
    )

    # If Jio has no language but source explicitly says
    # Hindi/English/Bhojpuri, allow it.
    if language not in ALLOWED_LANGUAGES:
        return None

    # --------------------------------------------------------
    # Genre
    # --------------------------------------------------------

    group = map_genre(
        ref.get(
            "genre",
            "",
        )
    )

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
# M3U OUTPUT
# ============================================================

def escape_m3u(value):
    value = clean_text(
        value
    )

    return value.replace(
        '"',
        "'",
    )


def build_extinf(
    entry,
    resolved,
):
    ref = resolved.get(
        "ref"
    )

    group = resolved[
        "group"
    ]

    language = resolved[
        "language"
    ]

    name = source_name(
        entry
    )

    logo = get_attr(
        entry,
        "tvg-logo",
        "logo",
    )

    tvg_id = source_tvg_id(
        entry
    )

    if not logo and ref:
        logo = ref.get(
            "logo",
            "",
        )

    # Keep Wizakor display name.
    # It is usually more useful than the old Jio name.

    attrs = []

    if tvg_id:
        attrs.append(
            f'tvg-id="{escape_m3u(tvg_id)}"'
        )
    elif ref:
        rid = clean_text(
            ref.get(
                "id",
                "",
            )
        )

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
# URL
# ============================================================

def normalize_url(url):
    return clean_text(
        url
    )


def url_key(url):
    return normalize_url(
        url
    )


# ============================================================
# SOURCE LOADING
# ============================================================

def load_sources(source_dir):
    entries = []

    source_path = Path(
        source_dir
    )

    # Local sources are allowed if workflow provides them.
    if source_path.exists():
        files = sorted(
            p
            for p in source_path.rglob("*")
            if (
                p.is_file()
                and p.suffix.lower()
                in {
                    ".m3u",
                    ".m3u8",
                    ".txt",
                }
            )
        )

        for path in files:
            try:
                text = path.read_text(
                    encoding="utf-8",
                    errors="replace",
                )

                parsed = parse_m3u(
                    text
                )

                print(
                    f"  {path}: "
                    f"{len(parsed)} entries"
                )

                entries.extend(
                    parsed
                )

            except Exception as exc:
                print(
                    f"  Failed {path}: "
                    f"{type(exc).__name__}: {exc}"
                )

    # If local files exist, still use the four configured
    # Wizakor sources when they are not already represented.
    print(
        "Fetching WizakorHD source playlists..."
    )

    for url in SOURCE_URLS:
        try:
            text = fetch_text(
                url
            )

            parsed = parse_m3u(
                text
            )

            print(
                f"  {url.rsplit('/', 1)[-1]}: "
                f"{len(parsed)} entries"
            )

            entries.extend(
                parsed
            )

        except Exception as exc:
            print(
                f"  Source failed: "
                f"{url}: "
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
            "from WizakorHD streams using "
            "JioTV/Tata Play references."
        )
    )

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

    # --------------------------------------------------------
    # JioTV
    # --------------------------------------------------------

    jio_refs = load_jiotv_reference()

    # --------------------------------------------------------
    # Tata Play identity reference
    # --------------------------------------------------------

    tata_refs = load_epg_reference(
        TATAPLAY_EPG_URL,
        "Tata Play",
    )

    all_refs = []

    all_refs.extend(
        jio_refs
    )

    all_refs.extend(
        tata_refs
    )

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
    # Resolve
    # --------------------------------------------------------

    resolved_entries = []

    stats = {
        "source": len(
            source_entries
        ),
        "indian": 0,
        "foreign_cricket": 0,
        "rejected": 0,
    }

    for entry in source_entries:
        url = normalize_url(
            entry.get(
                "url",
                "",
            )
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
            stats[
                "foreign_cricket"
            ] += 1
            priority = 1

        resolved_entries.append(
            (
                priority,
                entry,
                result,
            )
        )

    # Indian channels first
    resolved_entries.sort(
        key=lambda item: item[0]
    )

    # --------------------------------------------------------
    # Exact URL global dedup
    # --------------------------------------------------------

    seen_urls = set()

    final_entries = []

    for (
        priority,
        entry,
        result,
    ) in resolved_entries:

        url = normalize_url(
            entry.get(
                "url",
                "",
            )
        )

        key = url_key(
            url
        )

        if not key:
            continue

        if key in seen_urls:
            continue

        seen_urls.add(
            key
        )

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

    for (
        entry,
        result,
        url,
    ) in final_entries:

        group = result[
            "group"
        ]

        if group in grouped:
            grouped[group].append(
                (
                    entry,
                    result,
                    url,
                )
            )

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    for group in GROUPS:
        grouped[group].sort(
            key=lambda item: (
                normalize_name(
                    source_name(
                        item[0]
                    )
                ),
                item[2],
            )
        )

    # --------------------------------------------------------
    # Write
    # --------------------------------------------------------

    output = Path(
        args.output
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    lines = [
        "#EXTM3U",
        '#EXTVLCOPT:http-referrer=""',
    ]

    total = 0

    for group in GROUPS:
        for (
            entry,
            result,
            url,
        ) in grouped[group]:

            lines.append(
                build_extinf(
                    entry,
                    result,
                )
            )

            lines.append(
                url
            )

            total += 1

    output.write_text(
        "\n".join(lines)
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
        f"Source entries       : "
        f"{stats['source']}"
    )

    print(
        f"Indian matched       : "
        f"{stats['indian']}"
    )

    print(
        f"Foreign cricket      : "
        f"{stats['foreign_cricket']}"
    )

    print(
        f"Rejected              : "
        f"{stats['rejected']}"
    )

    print(
        f"Final unique streams  : "
        f"{total}"
    )

    print(
        f"Output                : "
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
```
