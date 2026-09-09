from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="qwen3:4b",
    temperature=0
)


def explain_change(result):
    if result["status"] == "UNCHANGED":
        return "No meaningful change detected."

    old_clause = result["old_clause"]
    new_clause = result["new_clause"]

    old_text = ""

    if old_clause:
        old_text = (
            old_clause["title"]
            + "\n"
            + old_clause["text"]
        )

    new_text = ""

    if new_clause:
        new_text = (
            new_clause["title"]
            + "\n"
            + new_clause["text"]
        )

    prompt = f"""
You are assisting with contract comparison.

Do not provide legal advice.

Explain the following contract change in simple language.

Status:
{result["status"]}

Old clause:
{old_text}

New clause:
{new_text}

Important detected changes:
{result["field_changes"]}

Risk level:
{result["risk"]}

Explain:
1. What changed
2. Why the change may matter
3. What should be reviewed carefully

Keep the response short and clear.
"""

    response = llm.invoke(prompt)

    return response.content


def answer_question(question, comparison_results):
    context = ""

    for result in comparison_results:
        context += "\nStatus: " + result["status"]
        context += "\nRisk: " + result["risk"]

        if result["old_clause"]:
            context += (
                "\nOld: "
                + result["old_clause"]["title"]
                + " "
                + result["old_clause"]["text"]
            )

        if result["new_clause"]:
            context += (
                "\nNew: "
                + result["new_clause"]["title"]
                + " "
                + result["new_clause"]["text"]
            )

        context += "\n"

    prompt = f"""
You are answering questions about two compared contracts.

Use only the information in the provided comparison.

Do not provide legal advice.

If the answer cannot be found in the comparison,
say that clearly.

Comparison:

{context}

Question:
{question}

Answer clearly and briefly.
"""

    response = llm.invoke(prompt)

    return response.content