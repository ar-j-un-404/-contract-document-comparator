from pathlib import Path

from extractor import extract_pdf_text
from cleaner import clean_text
from chunking import split_into_clauses
from embedding import create_embeddings
from matching import match_clauses
from comparator import compare_contracts
from llm import explain_change, answer_question
from report import print_report


def get_pdf_path(name):
    while True:
        pdf_path = Path(
            input(
                f"Enter path for PDF {name}: "
            )
        )

        if not pdf_path.exists():
            print("File does not exist")

        elif not pdf_path.is_file():
            print("Path is not a file")

        elif pdf_path.suffix.lower() != ".pdf":
            print("Only PDF files are allowed")

        else:
            print(
                f"PDF {name} is valid"
            )

            return pdf_path


def main():
    print("=" * 60)
    print("CONTRACT & DOCUMENT COMPARATOR")
    print("=" * 60)

    pdf_a = get_pdf_path("A")
    pdf_b = get_pdf_path("B")

    print("\nExtracting PDF text...")

    full_text_a = extract_pdf_text(pdf_a)
    full_text_b = extract_pdf_text(pdf_b)

    print("Cleaning text...")

    clean_text_a = clean_text(full_text_a)
    clean_text_b = clean_text(full_text_b)

    print("Splitting contracts into clauses...")

    clauses_a = split_into_clauses(
        clean_text_a
    )

    clauses_b = split_into_clauses(
        clean_text_b
    )

    print(
        f"PDF A clauses: {len(clauses_a)}"
    )

    print(
        f"PDF B clauses: {len(clauses_b)}"
    )

    print("Creating embeddings...")

    embeddings_a = create_embeddings(
        clauses_a
    )

    embeddings_b = create_embeddings(
        clauses_b
    )

    print("Matching clauses...")

    matches, unmatched_b = match_clauses(
        clauses_a,
        clauses_b,
        embeddings_a,
        embeddings_b
    )

    print("Comparing contracts...")

    results = compare_contracts(
        matches,
        unmatched_b
    )

    print("\nGenerating AI explanations...")

    for result in results:
        if result["status"] != "UNCHANGED":
            try:
                result["explanation"] = explain_change(
                    result
                )

            except Exception as error:
                result["explanation"] = (
                    "AI explanation unavailable: "
                    + str(error)
                )

    print_report(results)

    while True:
        print("\nOptions")
        print("1. Ask a question")
        print("2. View report again")
        print("3. Exit")

        choice = input(
            "\nEnter choice: "
        ).strip()

        if choice == "1":
            question = input(
                "Ask about the contracts: "
            )

            try:
                answer = answer_question(
                    question,
                    results
                )

                print("\nAnswer:")
                print(answer)

            except Exception as error:
                print(
                    "Unable to contact Ollama:",
                    error
                )

        elif choice == "2":
            print_report(results)

        elif choice == "3":
            print("Exiting comparator.")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()