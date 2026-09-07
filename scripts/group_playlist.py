LANG_ALIASES = {
    "hindi": {"hindi", "hin"},
    "english": {"english", "eng"},
    "bhojpuri": {"bhojpuri", "bho"},
}

def has_language(channel, language):
    values = {
        str(x).strip().lower()
        for x in (channel.get("languages") or [])
    }

    return bool(values & LANG_ALIASES[language])
