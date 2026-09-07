python - <<'PY'
import json, urllib.request, re

def get(u):
    r = urllib.request.Request(u, headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(r, timeout=60) as x:
        return json.load(x)

c = get("https://iptv-org.github.io/api/channels.json")
f = get("https://iptv-org.github.io/api/feeds.json")
s = get("https://iptv-org.github.io/api/streams.json")

# ---------- RULES ----------
ALLOWED_INDIA = {"hindi", "hin", "english", "eng", "bhojpuri", "bho"}

REGIONAL = {
    "tamil","tam","telugu","tel","bengali","ben","marathi","mar",
    "gujarati","guj","kannada","kan","malayalam","mal","punjabi","pan",
    "odia","oriya","ori","assamese","asm","urdu","urd","kashmiri","kas",
    "nepali","nep","konkani","kok","sanskrit","san","sindhi","snd",
    "maithili","mai","dogri","doi","manipuri","mni"
}

BAD = ("evidya","pmevidya","swayamprabha","vandegujarat")

# ---------- HINDI FEED IDS ----------
hindi_ids = set()

for x in f:
    langs = x.get("languages") or []
    if isinstance(langs, str):
        langs = [langs]

    langs = {
        str(a).lower().strip()
        for a in langs
    }

    if {"hindi", "hin"} & langs:
        if x.get("channel"):
            hindi_ids.add(str(x["channel"]))

# ---------- INDEX ----------
channels = {
    str(x.get("id")): x
    for x in c
    if x.get("id") is not None
}

feeds = {}
for x in f:
    if x.get("channel"):
        feeds[str(x["channel"])] = x

# ---------- URL EXTRACT ----------
def stream_url(x):
    for k in ("url", "stream", "src", "hls"):
        v = x.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""

def langs_of(ch, feed):
    out = set()

    for obj in (ch, feed):
        if not obj:
            continue

        v = obj.get("languages") or []
        if isinstance(v, str):
            v = [v]

        for a in v:
            out.add(str(a).lower().strip())

    return out

def text_of(ch, feed, st):
    vals = []

    for obj in (ch, feed, st):
        if not obj:
            continue

        for k in (
            "name","title","network","description",
            "category","categories","tags"
        ):
            v = obj.get(k)

            if isinstance(v, list):
                vals += [str(a) for a in v]
            elif v:
                vals.append(str(v))

    return " ".join(vals).lower()

def excluded(ch, feed, st):
    t = re.sub(r"[^a-z0-9]", "", text_of(ch, feed, st))
    return any(x in t for x in BAD)

def regional(ch, feed):
    return bool(langs_of(ch, feed) & REGIONAL)

# ---------- CRICKET ----------
CRICKET = (
    "cricket",
    "willow",
    "fox cricket",
    "sky sports cricket",
    "supersport cricket",
    "ten cricket",
    "t sports cricket",
    "icc cricket",
    "ipl",
    "bcci",
    "big bash",
    "bbl",
    "psl",
    "wpl",
    "cpl",
    "test cricket",
    "county cricket",
    "the hundred"
)

def is_cricket(ch, feed, st):
    t = text_of(ch, feed, st)
    return any(x in t for x in CRICKET)

# ---------- RESULT ----------
result = []
seen_urls = set()
name_count = {}

for st in s:
    cid = st.get("channel")
    if cid is None:
        continue

    cid = str(cid)

    ch = channels.get(cid)
    if not ch:
        continue

    feed = feeds.get(cid)

    if excluded(ch, feed, st):
        continue

    url = stream_url(st)
    if not url:
        continue

    # SAME STREAM = REMOVE GLOBALLY
    if url in seen_urls:
        continue

    langs = langs_of(ch, feed)
    country = str(ch.get("country") or "").upper()

    group = None

    # ---------- INDIA ----------
    if country == "IN":

        # Regional language = NEVER ADD
        if regional(ch, feed):
            continue

        if cid in hindi_ids or langs & {"hindi", "hin"}:
            group = "India - Hindi"

        elif langs & {"english", "eng"}:
            group = "India - English"

        elif langs & {"bhojpuri", "bho"}:
            group = "India - Bhojpuri"

        else:
            continue

    # ---------- FOREIGN HINDI ----------
    elif country in {"GB","US","CA","AE","QA","SA","BH","KW","OM"}:

        if not (cid in hindi_ids or langs & {"hindi","hin"}):
            continue

        group = {
            "GB":"UK - Hindi",
            "US":"USA - Hindi",
            "CA":"Canada - Hindi",
            "AE":"Middle East - Hindi",
            "QA":"Middle East - Hindi",
            "SA":"Middle East - Hindi",
            "BH":"Middle East - Hindi",
            "KW":"Middle East - Hindi",
            "OM":"Middle East - Hindi"
        }.get(country)

        if not group:
            continue

    # ---------- GLOBAL CRICKET ----------
    elif is_cricket(ch, feed, st):
        group = "Sports - Cricket"

    else:
        continue

    # ---------- NAME ----------
    base = str(
        ch.get("name")
        or st.get("title")
        or "Unknown"
    ).strip()

    key = (group, base.lower())

    name_count[key] = name_count.get(key, 0) + 1
    n = name_count[key]

    name = base if n == 1 else f"{base} {n}"

    seen_urls.add(url)

    result.append({
        "group": group,
        "name": name,
        "url": url,
        "channel_id": cid
    })

# ---------- PRINT ----------
order = [
    "India - Hindi",
    "India - English",
    "India - Bhojpuri",
    "UK - Hindi",
    "USA - Hindi",
    "Canada - Hindi",
    "Middle East - Hindi",
    "Sports - Cricket"
]

for g in order:
    a = [x for x in result if x["group"] == g]
    print(f"{g}: {len(a)}")

print()
print("TOTAL UNIQUE CHANNELS:", len(result))
print("EXPECTED:", 609)
PY
