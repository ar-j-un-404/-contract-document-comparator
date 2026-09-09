import difflib


def highlight_diff(old_text, new_text):
    old_words = old_text.split()
    new_words = new_text.split()

    matcher = difflib.SequenceMatcher(
        None,
        old_words,
        new_words
    )

    old_result = []
    new_result = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():

        if tag == "equal":
            old_result.extend(
                old_words[i1:i2]
            )

            new_result.extend(
                new_words[j1:j2]
            )

        elif tag == "replace":
            old_part = " ".join(
                old_words[i1:i2]
            )

            new_part = " ".join(
                new_words[j1:j2]
            )

            old_result.append(
                f"**[{old_part}]**"
            )

            new_result.append(
                f"**[{new_part}]**"
            )

        elif tag == "delete":
            old_part = " ".join(
                old_words[i1:i2]
            )

            old_result.append(
                f"**[{old_part}]**"
            )

        elif tag == "insert":
            new_part = " ".join(
                new_words[j1:j2]
            )

            new_result.append(
                f"**[{new_part}]**"
            )

    return (
        " ".join(old_result),
        " ".join(new_result)
    )