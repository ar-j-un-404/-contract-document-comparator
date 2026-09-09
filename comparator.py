from field_detector import compare_fields


IMPORTANT_KEYWORDS = [
    "termination",
    "liability",
    "payment",
    "confidentiality",
    "indemnity",
    "penalty",
    "notice",
    "obligation",
    "data protection"
]


def normalize_clause(text):
    return " ".join(
        text.lower().split()
    )


def calculate_risk(status, clause, field_changes):
    text = (
        clause["title"] + " " + clause["text"]
    ).lower()

    score = 0

    if status == "MODIFIED":
        score += 2

    elif status in ["ADDED", "REMOVED"]:
        score += 3

    for keyword in IMPORTANT_KEYWORDS:
        if keyword in text:
            score += 1

    if "money" in field_changes:
        score += 2

    if "notice_period" in field_changes:
        score += 2

    if "dates" in field_changes:
        score += 1

    if "obligations" in field_changes:
        score += 2

    if score >= 5:
        return "HIGH"

    elif score >= 3:
        return "MEDIUM"

    return "LOW"


def compare_contracts(matches, unmatched_b):
    results = []

    for match in matches:
        clause_a = match["clause_a"]
        clause_b = match["clause_b"]

        if clause_b is None:
            status = "REMOVED"
            field_changes = {}

            risk = calculate_risk(
                status,
                clause_a,
                field_changes
            )

            results.append(
                {
                    "status": status,
                    "old_clause": clause_a,
                    "new_clause": None,
                    "similarity": 0,
                    "field_changes": field_changes,
                    "risk": risk
                }
            )

            continue

        text_a = normalize_clause(
            clause_a["text"]
        )

        text_b = normalize_clause(
            clause_b["text"]
        )

        if text_a == text_b:
            status = "UNCHANGED"
        else:
            status = "MODIFIED"

        field_changes = compare_fields(
            clause_a["text"],
            clause_b["text"]
        )

        risk = calculate_risk(
            status,
            clause_b,
            field_changes
        )

        results.append(
            {
                "status": status,
                "old_clause": clause_a,
                "new_clause": clause_b,
                "similarity": match["similarity"],
                "field_changes": field_changes,
                "risk": risk
            }
        )

    for clause_b in unmatched_b:
        status = "ADDED"
        field_changes = {}

        risk = calculate_risk(
            status,
            clause_b,
            field_changes
        )

        results.append(
            {
                "status": status,
                "old_clause": None,
                "new_clause": clause_b,
                "similarity": 0,
                "field_changes": field_changes,
                "risk": risk
            }
        )

    return results