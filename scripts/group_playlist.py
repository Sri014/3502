```python
#!/usr/bin/env python3

import gzip
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit

# ============================================================
# STREAM SOURCES - ONLY THESE 4
# ============================================================

SOURCE_URLS = [
    "https://raw.githubusercontent.com/wizakorhd/iptv/refs/heads/main/playlist-hindi.m3u",
    "https://raw.githubusercontent.com/wizakorhd/iptv/refs/heads/main/playlist-english-india.m3u",
    "https://raw.githubusercontent.com/wizakorhd/iptv/refs/heads/main/playlist-top.m3u",
    "https://raw.githubusercontent.com/wizakorhd/iptv/refs/heads/main/playlist.m3u",
]

# ============================================================
# REFERENCE DATA
#
# JioTV EPG:
# https://raw.githubusercontent.com/mitthu786/tvepg/main/jiotv/epg.xml.gz
#
# Tata Play EPG:
# https://raw.githubusercontent.com/mitthu786/tvepg/main/tataplay/epg.xml.gz
# ============================================================

JIO_EPG = (
    "https://raw.githubusercontent.com/mitthu786/tvepg/"
    "main/jiotv/epg.xml.gz"
)

TATA_EPG = (
    "https://raw.githubusercontent.com/mitthu786/tvepg/"
    "main/tataplay/epg.xml.gz"
)

# ============================================================
# FINAL GROUPS
# ============================================================

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

ALLOWED_LANG = {
    "hindi",
    "english",
    "bhojpuri",
}

BAD_LANG = {
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
    "chhattisgarhi",
}

# ============================================================
# DOWNLOAD
# ============================================================

def fetch(url):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "*/*",
        },
    )

    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def norm(value):
    value = str(value or "").lower()

    value = value.replace("&", " and ")

    # Remove quality/technical suffixes.
    value = re.sub(
        r"\b("
        r"hd|fhd|uhd|4k|8k|sd|"
        r"1080p|720p|576p|480p|"
        r"hevc|h265|h264"
        r")\b",
        " ",
        value,
        flags=re.I,
    )

    value = re.sub(r"[^a-z0-9\u0900-\u097f]+", " ", value)
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def compact(value):
    return norm(value).replace(" ", "")


def tokens(value):
    return set(norm(value).split())


# ============================================================
# LANGUAGE
# ============================================================

def clean_language(value):
    value = norm(value)

    if "bhojpuri" in value:
        return "Bhojpuri"

    if "hindi" in value:
        return "Hindi"

    if "english" in value:
        return "English"

    return ""


def bad_language(value):
    value = norm(value)

    for lang in BAD_LANG:
        if re.search(
            r"\b" + re.escape(lang) + r"\b",
            value
        ):
            return True

    return False


# ============================================================
# GENRE -> OUR 10 GROUPS
# ============================================================

def map_genre(genre):
    g = norm(genre)

    if not g:
        return None

    # Exact / strong genre mapping.
    if "news" in g:
        return "News"

    if "business" in g:
        return "Business"

    if "sports" in g or "sport" in g:
        return "Sports"

    if "movie" in g or "cinema" in g:
        return "Movies"

    if "music" in g:
        return "Music"

    if "kid" in g or "children" in g:
        return "Kids"

    if "science" in g:
        return "Science"

    if "lifestyle" in g:
        return "Lifestyle"

    if "infotainment" in g:
        return "Infotainment"

    if "entertainment" in g:
        return "Entertainment"

    return None


# ============================================================
# XMLTV REFERENCE PARSER
# ============================================================

def parse_epg(raw):
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)

    root = ET.fromstring(raw)

    channels = []

    for ch in root.findall(".//channel"):
        channel_id = (
            ch.attrib.get("id", "").strip()
        )

        names = []

        for dn in ch.findall("./display-name"):
            if dn.text:
                names.append(
                    dn.text.strip()
                )

        if not names:
            continue

        name = names[0]

        # XMLTV normally doesn't expose Jio genre/lang
        # directly, so collect any available metadata.
        text = " ".join(names)

        channels.append({
            "id": channel_id,
            "name": name,
            "names": names,
            "text": text,
            "norm": norm(name),
            "compact": compact(name),
        })

    return channels


# ============================================================
# LOAD JIO + TATA REFERENCES
# ============================================================

def load_reference():
    refs = []

    print("Fetching JioTV reference...")

    try:
        jio_raw = fetch(JIO_EPG)
        jio = parse_epg(jio_raw)

        for item in jio:
            item["provider"] = "JioTV"
            refs.append(item)

        print(
            "  JioTV channels:",
            len(jio)
        )

    except Exception as e:
        print(
            "  JioTV reference error:",
            e
        )

    print("Fetching Tata Play reference...")

    try:
        tata_raw = fetch(TATA_EPG)
        tata = parse_epg(tata_raw)

        for item in tata:
            item["provider"] = "TataPlay"
            refs.append(item)

        print(
            "  Tata Play channels:",
            len(tata)
        )

    except Exception as e:
        print(
            "  Tata Play reference error:",
            e
        )

    if not refs:
        print(
            "ERROR: No JioTV/Tata Play reference loaded."
        )
        sys.exit(1)

    return refs


# ============================================================
# CHANNEL NAME MATCH
#
# IMPORTANT:
# NO GENERIC KEYWORD MATCH.
#
# Only a strong reference-name match is accepted.
# ============================================================

def match_reference(source_name, refs):
    src = norm(source_name)
    src_compact = compact(source_name)
    src_tokens = tokens(source_name)

    if not src:
        return None

    # --------------------------------------------------------
    # 1. Exact normalized name
    # --------------------------------------------------------

    for ref in refs:
        if src == ref["norm"]:
            return ref

    # --------------------------------------------------------
    # 2. Exact compact name
    # --------------------------------------------------------

    for ref in refs:
        if src_compact == ref["compact"]:
            return ref

    # --------------------------------------------------------
    # 3. Strong token match
    #
    # All meaningful reference tokens must exist in source.
    # Single generic words are never sufficient.
    # --------------------------------------------------------

    generic = {
        "tv",
        "hd",
        "sd",
        "channel",
        "india",
        "live",
        "network",
        "the",
    }

    best = None
    best_score = -1

    for ref in refs:
        rt = {
            x for x in tokens(ref["name"])
            if x not in generic
        }

        if not rt:
            continue

        if not rt.issubset(src_tokens):
            continue

        # Require at least 2 meaningful tokens unless
        # the full source/reference normalized name is equal.
        if len(rt) < 2:
            continue

        score = len(rt)

        # Prefer more specific/longer names.
        score += len(ref["name"]) / 10000.0

        if score > best_score:
            best_score = score
            best = ref

    return best


# ============================================================
# M3U PARSER
# ============================================================

def parse_m3u(text, source):
    entries = []

    info = None
    name = ""

    for raw in text.splitlines():
        line = raw.strip()

        if not line:
            continue

        if line.startswith("#EXTINF"):
            info = line

            if "," in line:
                name = line.split(",", 1)[1].strip()
            else:
                name = ""

            continue

        if line.startswith("#"):
            continue

        if info is None:
            continue

        entries.append({
            "info": info,
            "name": name,
            "url": line,
            "source": source,
        })

        info = None
        name = ""

    return entries


# ============================================================
# EXTINF ATTRIBUTES
# ============================================================

def parse_attrs(info):
    attrs = {}

    for key, value in re.findall(
        r'([\w-]+)="([^"]*)"',
        info
    ):
        attrs[key.lower()] = value

    return attrs


def make_extinf(entry, group, language, name):
    attrs = parse_attrs(entry["info"])

    attrs["tvg-name"] = name
    attrs["group-title"] = group
    attrs["tvg-language"] = language

    preferred = [
        "tvg-id",
        "tvg-name",
        "tvg-logo",
        "tvg-language",
        "group-title",
    ]

    out = []
    used = set()

    for key in preferred:
        if key in attrs:
            out.append(
                f'{key}="{attrs[key]}"'
            )
            used.add(key)

    for key, value in attrs.items():
        if key not in used:
            out.append(
                f'{key}="{value}"'
            )

    return (
        "#EXTINF:-1 "
        + " ".join(out)
        + ","
        + name
    )


# ============================================================
# SOURCE LANGUAGE
# ============================================================

def source_language(entry):
    attrs = parse_attrs(
        entry["info"]
    )

    explicit = clean_language(
        attrs.get("tvg-language", "")
    )

    if explicit:
        return explicit

    text = (
        entry["info"]
        + " "
        + entry["name"]
        + " "
        + entry["source"]
    )

    return clean_language(text)


# ============================================================
# FOREIGN CRICKET EXCEPTION
# ============================================================

def is_cricket(name):
    return "cricket" in norm(name)


# ============================================================
# MAIN
# ============================================================

def main():
    output = "playlist.m3u"

    if "-o" in sys.argv:
        pos = sys.argv.index("-o")

        if pos + 1 < len(sys.argv):
            output = sys.argv[pos + 1]

    print()
    print("==============================================")
    print(" STRICT JioTV + Tata Play CHANNEL MATCHER")
    print("==============================================")

    refs = load_reference()

    all_entries = []

    # --------------------------------------------------------
    # FETCH ONLY REQUESTED WIZAKORHD PLAYLISTS
    # --------------------------------------------------------

    for source_url in SOURCE_URLS:
        source = Path(
            urlsplit(source_url).path
        ).name

        print()
        print("Fetching:", source)

        try:
            raw = fetch(source_url)

            text = raw.decode(
                "utf-8",
                errors="replace"
            )

            entries = parse_m3u(
                text,
                source
            )

            print(
                "  entries:",
                len(entries)
            )

            all_entries.extend(entries)

        except Exception as e:
            print(
                "  ERROR:",
                e
            )

    print()
    print(
        "Total source entries:",
        len(all_entries)
    )

    # --------------------------------------------------------
    # FILTER + MATCH + DEDUP
    # --------------------------------------------------------

    final = []

    # Exact URL is globally unique.
    seen_urls = set()

    no_match = 0
    bad_lang = 0
    bad_group = 0
    duplicate = 0

    for entry in all_entries:

        name = entry["name"].strip()
        url = entry["url"].strip()

        if not name or not url:
            continue

        # ----------------------------------------------------
        # INDIAN IDENTITY MUST MATCH JIO/TATA
        # ----------------------------------------------------

        ref = match_reference(
            name,
            refs
        )

        if ref is None:
            # Foreign/unmatched channel.
            # Cricket is the ONLY exception.
            if not is_cricket(name):
                no_match += 1
                continue

            # Foreign cricket allowed.
            final_name = name
            language = (
                source_language(entry)
                or "English"
            )
            group = "Sports"

        else:
            # ------------------------------------------------
            # LANGUAGE
            # ------------------------------------------------

            combined = (
                ref["name"]
                + " "
                + ref["text"]
                + " "
                + entry["info"]
                + " "
                + entry["name"]
            )

            if bad_language(combined):
                bad_lang += 1
                continue

            language = source_language(entry)

            # Reference can identify channel even when source
            # doesn't contain tvg-language.
            if not language:
                language = clean_language(
                    combined
                )

            if language.lower() not in ALLOWED_LANG:
                bad_lang += 1
                continue

            # ------------------------------------------------
            # GROUP
            # ------------------------------------------------
            #
            # Source group-title is NEVER used.
            #
            # EPG XML may expose category indirectly; when it
            # cannot, only use the channel's reference metadata
            # where available.
            # ------------------------------------------------

            group = None

            # Match name against known EPG/reference text.
            ref_text = norm(
                ref["name"]
                + " "
                + ref["text"]
            )

            # Exact genre words only.
            if "business" in ref_text:
                group = "Business"

            elif "sports" in ref_text:
                group = "Sports"

            elif "news" in ref_text:
                group = "News"

            elif (
                "movie" in ref_text
                or "cinema" in ref_text
            ):
                group = "Movies"

            elif "music" in ref_text:
                group = "Music"

            elif (
                "kids" in ref_text
                or "children" in ref_text
            ):
                group = "Kids"

            elif "science" in ref_text:
                group = "Science"

            elif "lifestyle" in ref_text:
                group = "Lifestyle"

            elif "infotainment" in ref_text:
                group = "Infotainment"

            elif "entertainment" in ref_text:
                group = "Entertainment"

            # If this is a sports channel by actual name,
            # sports is still safe.
            if group is None and is_cricket(ref["name"]):
                group = "Sports"

            if group not in GROUPS:
                bad_group += 1
                continue

            final_name = ref["name"]

        # ----------------------------------------------------
        # EXACT GLOBAL URL DEDUP
        # ----------------------------------------------------

        if url in seen_urls:
            duplicate += 1
            continue

        seen_urls.add(url)

        final.append({
            "name": final_name,
            "language": language,
            "group": group,
            "url": url,
            "entry": entry,
        })

    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    order = {
        group: i
        for i, group in enumerate(GROUPS)
    }

    final.sort(
        key=lambda x: (
            order[x["group"]],
            norm(x["name"]),
            x["url"],
        )
    )

    # --------------------------------------------------------
    # WRITE
    # --------------------------------------------------------

    with open(
        output,
        "w",
        encoding="utf-8",
        newline="\n"
    ) as fp:

        fp.write("#EXTM3U\n")

        current = None

        for item in final:

            if item["group"] != current:
                current = item["group"]

                fp.write(
                    f"\n# ===== {current} =====\n"
                )

            fp.write(
                make_extinf(
                    item["entry"],
                    item["group"],
                    item["language"],
                    item["name"],
                )
                + "\n"
            )

            fp.write(
                item["url"]
                + "\n"
            )

    # --------------------------------------------------------
    # STATS
    # --------------------------------------------------------

    counts = {
        group: 0
        for group in GROUPS
    }

    for item in final:
        counts[item["group"]] += 1

    print()
    print("==============================================")
    print(" FINAL RESULT")
    print("==============================================")

    for group in GROUPS:
        print(
            f"{group:15} : {counts[group]}"
        )

    print("----------------------------------------------")
    print("Source entries :", len(all_entries))
    print("Final entries  :", len(final))
    print("No Jio/Tata match:", no_match)
    print("Bad language   :", bad_lang)
    print("Bad group      :", bad_group)
    print("Duplicates     :", duplicate)
    print("Output         :", output)
    print("==============================================")


if __name__ == "__main__":
    main()
```
