from argostranslate import translate


def translate_text(text, source="en", target="ja"):
    if not text:
        return ""
    return translate.translate(text, source, target)
