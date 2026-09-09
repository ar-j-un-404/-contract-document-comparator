from sklearn.metrics.pairwise import cosine_similarity


def match_clauses(
    clauses_a,
    clauses_b,
    embeddings_a,
    embeddings_b,
    threshold=0.55
):
    similarity_matrix = cosine_similarity(
        embeddings_a,
        embeddings_b
    )

    matches = []

    used_b = set()

    for i, clause_a in enumerate(clauses_a):
        best_index = -1
        best_score = -1

        for j, clause_b in enumerate(clauses_b):
            if j in used_b:
                continue

            score = similarity_matrix[i][j]

            if score > best_score:
                best_score = score
                best_index = j

        if best_index != -1 and best_score >= threshold:
            used_b.add(best_index)

            matches.append(
                {
                    "clause_a": clause_a,
                    "clause_b": clauses_b[best_index],
                    "similarity": float(best_score)
                }
            )

        else:
            matches.append(
                {
                    "clause_a": clause_a,
                    "clause_b": None,
                    "similarity": 0
                }
            )

    unmatched_b = []

    for j, clause_b in enumerate(clauses_b):
        if j not in used_b:
            unmatched_b.append(clause_b)

    return matches, unmatched_b