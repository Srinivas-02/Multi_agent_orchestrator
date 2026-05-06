import re


def analyze_text(text: str) -> dict:
    words = re.findall(r"\b[\w']+\b", text)
    sentences = re.findall(r"[^.!?]+[.!?]?", text.strip())

    return {
        "characters": len(text),
        "characters_without_spaces": len(text.replace(" ", "")),
        "words": len(words),
        "sentences": len([sentence for sentence in sentences if sentence.strip()]),
        "lines": len(text.splitlines()) if text else 0,
    }
