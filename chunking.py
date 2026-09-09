import re


def split_into_clauses(text):
    pattern = r"(?m)^(\d+(?:\.\d+)*)\.\s+([^\n]+)"

    matches = list(re.finditer(pattern, text))

    clauses = []

    if not matches:
        return [
            {
                "number": "1",
                "title": "Document",
                "text": text
            }
        ]

    for i in range(len(matches)):
        current_match = matches[i]

        number = current_match.group(1)
        title = current_match.group(2).strip()

        start = current_match.end()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        clause_text = text[start:end].strip()

        clauses.append(
            {
                "number": number,
                "title": title,
                "text": clause_text
            }
        )

    return clauses