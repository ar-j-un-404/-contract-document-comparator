from sentence_transformers import SentenceTransformer


_model = None


def get_model():
    global _model

    if _model is None:
        _model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    return _model


def create_embeddings(clauses):
    model = get_model()

    texts = []

    for clause in clauses:
        combined_text = (
            clause["title"]
            + " "
            + clause["text"]
        )

        texts.append(combined_text)

    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    return embeddings