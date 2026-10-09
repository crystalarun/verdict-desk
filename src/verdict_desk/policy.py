from __future__ import annotations

import re

JAILBREAK = re.compile(
    r"(ignore (all|any|previous|above) (instructions|rules)|you are now|jailbreak|"
    r"system prompt|pretend you have no restrictions|override (the )?policy)",
    re.I,
)
EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
# GCC mobiles: 05xxxxxxxx or +9715xxxxxxxx
PHONE = re.compile(r"(?:\+971|0)\s*5\d{1}[\s-]?\d{3}[\s-]?\d{4}")
EMIRATES_ID = re.compile(r"\b784-\d{4}-\d{7}-\d\b")


def mask_pii(text: str) -> str:
    text = EMAIL.sub("[EMAIL]", text)
    text = PHONE.sub("[PHONE]", text)
    text = EMIRATES_ID.sub("[ID]", text)
    return text


def inspect_question(question: str) -> str | None:
    if JAILBREAK.search(question):
        return "jailbreak_attempt"
    return None
