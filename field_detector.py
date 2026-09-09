import re


def extract_money(text):
    patterns = [
        r"\$\s?[\d,]+(?:\.\d+)?",
        r"USD\s?[\d,]+(?:\.\d+)?",
        r"INR\s?[\d,]+(?:\.\d+)?",
        r"₹\s?[\d,]+(?:\.\d+)?"
    ]

    results = []

    for pattern in patterns:
        results.extend(
            re.findall(
                pattern,
                text,
                flags=re.IGNORECASE
            )
        )

    return results


def extract_notice_periods(text):
    pattern = (
        r"\b(?:notice|terminate|termination)"
        r"[^\n.]{0,60}?"
        r"\b\d+\s+"
        r"(?:day|days|week|weeks|month|months)\b"
    )

    matches = re.findall(
        pattern,
        text,
        flags=re.IGNORECASE
    )

    periods = []

    for match in matches:
        duration = re.search(
            r"\b\d+\s+(?:day|days|week|weeks|month|months)\b",
            match,
            flags=re.IGNORECASE
        )

        if duration:
            periods.append(duration.group())

    return periods


def extract_dates(text):
    patterns = [
        r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
        r"\b\d{1,2}-\d{1,2}-\d{2,4}\b",
        (
            r"\b(?:January|February|March|April|May|June|July|"
            r"August|September|October|November|December)"
            r"\s+\d{1,2},?\s+\d{4}\b"
        )
    ]

    results = []

    for pattern in patterns:
        results.extend(
            re.findall(
                pattern,
                text,
                flags=re.IGNORECASE
            )
        )

    return results


def detect_obligations(text):
    words = [
        "shall",
        "must",
        "required",
        "responsible",
        "obligation"
    ]

    detected = []

    lower_text = text.lower()

    for word in words:
        if word in lower_text:
            detected.append(word)

    return detected


def compare_fields(text_a, text_b):
    changes = {}

    money_a = extract_money(text_a)
    money_b = extract_money(text_b)

    if money_a != money_b:
        changes["money"] = {
            "old": money_a,
            "new": money_b
        }

    notice_a = extract_notice_periods(text_a)
    notice_b = extract_notice_periods(text_b)

    if notice_a != notice_b:
        changes["notice_period"] = {
            "old": notice_a,
            "new": notice_b
        }

    dates_a = extract_dates(text_a)
    dates_b = extract_dates(text_b)

    if dates_a != dates_b:
        changes["dates"] = {
            "old": dates_a,
            "new": dates_b
        }

    obligations_a = detect_obligations(text_a)
    obligations_b = detect_obligations(text_b)

    if obligations_a != obligations_b:
        changes["obligations"] = {
            "old": obligations_a,
            "new": obligations_b
        }

    return changes