import streamlit as st
from pathlib import Path
import tempfile

from extractor import extract_pdf_text
from cleaner import clean_text
from chunking import split_into_clauses
from embedding import create_embeddings
from matching import match_clauses
from comparator import compare_contracts
from llm import explain_change, answer_question
from diff_utils import highlight_diff
from exporter import results_to_json


st.set_page_config(
    page_title="Contract Comparator",
    layout="wide"
)


st.title("Contract & Document Comparator")

st.write(
    "Compare two contracts and detect modified, "
    "added, removed, and unchanged clauses."
)

st.caption(
    "AI-assisted document comparison. "
    
)


def save_uploaded_file(uploaded_file):
    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    temp_file.write(
        uploaded_file.getbuffer()
    )

    temp_file.close()

    return Path(temp_file.name)


def process_contracts(
    pdf_a_path,
    pdf_b_path
):
    full_text_a = extract_pdf_text(
        pdf_a_path
    )

    full_text_b = extract_pdf_text(
        pdf_b_path
    )

    if not full_text_a.strip():
        raise ValueError(
            "Contract A contains no extractable text."
        )

    if not full_text_b.strip():
        raise ValueError(
            "Contract B contains no extractable text."
        )

    clean_a = clean_text(
        full_text_a
    )

    clean_b = clean_text(
        full_text_b
    )

    clauses_a = split_into_clauses(
        clean_a
    )

    clauses_b = split_into_clauses(
        clean_b
    )

    embeddings_a = create_embeddings(
        clauses_a
    )

    embeddings_b = create_embeddings(
        clauses_b
    )

    matches, unmatched_b = match_clauses(
        clauses_a,
        clauses_b,
        embeddings_a,
        embeddings_b
    )

    return compare_contracts(
        matches,
        unmatched_b
    )


upload_col1, upload_col2 = st.columns(2)

with upload_col1:
    pdf_a = st.file_uploader(
        "Upload Contract A",
        type=["pdf"],
        key="pdf_a"
    )

with upload_col2:
    pdf_b = st.file_uploader(
        "Upload Contract B",
        type=["pdf"],
        key="pdf_b"
    )


if st.button(
    "Compare Contracts",
    type="primary",
    use_container_width=True
):
    if pdf_a is None or pdf_b is None:
        st.warning(
            "Upload both contracts first."
        )

    elif pdf_a.name == pdf_b.name:
        st.warning(
            "The uploaded files have the same filename. "
            "Make sure they are actually different versions."
        )

    else:
        try:
            path_a = save_uploaded_file(
                pdf_a
            )

            path_b = save_uploaded_file(
                pdf_b
            )

            with st.spinner(
                "Comparing contracts..."
            ):
                results = process_contracts(
                    path_a,
                    path_b
                )

            st.session_state[
                "results"
            ] = results

            keys_to_remove = []

            for key in st.session_state:
                if key.startswith(
                    "explanation_"
                ):
                    keys_to_remove.append(
                        key
                    )

            for key in keys_to_remove:
                del st.session_state[key]

            st.success(
                "Comparison completed."
            )

        except Exception as error:
            st.error(
                f"Comparison failed: {error}"
            )


if "results" in st.session_state:
    results = st.session_state[
        "results"
    ]

    modified = sum(
        1 for r in results
        if r["status"] == "MODIFIED"
    )

    added = sum(
        1 for r in results
        if r["status"] == "ADDED"
    )

    removed = sum(
        1 for r in results
        if r["status"] == "REMOVED"
    )

    unchanged = sum(
        1 for r in results
        if r["status"] == "UNCHANGED"
    )

    high_risk = sum(
        1 for r in results
        if r["risk"] == "HIGH"
    )

    st.divider()

    st.subheader(
        "Comparison Summary"
    )

    col1, col2, col3, col4, col5 = (
        st.columns(5)
    )

    col1.metric(
        "Modified",
        modified
    )

    col2.metric(
        "Added",
        added
    )

    col3.metric(
        "Removed",
        removed
    )

    col4.metric(
        "Unchanged",
        unchanged
    )

    col5.metric(
        "High Risk",
        high_risk
    )

    st.divider()

    filter_col1, filter_col2 = (
        st.columns(2)
    )

    with filter_col1:
        status_filter = (
            st.selectbox(
                "Filter by status",
                [
                    "ALL",
                    "MODIFIED",
                    "ADDED",
                    "REMOVED",
                    "UNCHANGED"
                ]
            )
        )

    with filter_col2:
        risk_filter = (
            st.selectbox(
                "Filter by risk",
                [
                    "ALL",
                    "HIGH",
                    "MEDIUM",
                    "LOW"
                ]
            )
        )

    st.subheader(
        "Clause Comparison"
    )

    visible_results = 0

    for index, result in enumerate(
        results,
        start=1
    ):
        if (
            status_filter != "ALL"
            and result["status"]
            != status_filter
        ):
            continue

        if (
            risk_filter != "ALL"
            and result["risk"]
            != risk_filter
        ):
            continue

        visible_results += 1

        old_clause = result[
            "old_clause"
        ]

        new_clause = result[
            "new_clause"
        ]

        if new_clause:
            title = new_clause[
                "title"
            ]

        elif old_clause:
            title = old_clause[
                "title"
            ]

        else:
            title = (
                f"Clause {index}"
            )

        heading = (
            f"{title} | "
            f"{result['status']} | "
            f"Risk: {result['risk']}"
        )

        with st.expander(
            heading,
            expanded=(
                result["status"]
                != "UNCHANGED"
            )
        ):
            if result["similarity"]:
                st.write(
                    "Similarity:",
                    f"{result['similarity'] * 100:.2f}%"
                )

            left, right = st.columns(2)

            if (
                old_clause
                and new_clause
                and result["status"]
                == "MODIFIED"
            ):
                old_highlighted, (
                    new_highlighted
                ) = highlight_diff(
                    old_clause["text"],
                    new_clause["text"]
                )

            else:
                old_highlighted = (
                    old_clause["text"]
                    if old_clause
                    else ""
                )

                new_highlighted = (
                    new_clause["text"]
                    if new_clause
                    else ""
                )

            with left:
                st.markdown(
                    "### Contract A"
                )

                if old_clause:
                    st.markdown(
                        f"**{old_clause['title']}**"
                    )

                    st.markdown(
                        old_highlighted
                    )

                else:
                    st.info(
                        "This clause did not "
                        "exist in Contract A."
                    )

            with right:
                st.markdown(
                    "### Contract B"
                )

                if new_clause:
                    st.markdown(
                        f"**{new_clause['title']}**"
                    )

                    st.markdown(
                        new_highlighted
                    )

                else:
                    st.info(
                        "This clause was "
                        "removed from Contract B."
                    )

            if result[
                "field_changes"
            ]:
                st.markdown(
                    "### Important Changes"
                )

                for field, values in (
                    result[
                        "field_changes"
                    ].items()
                ):
                    st.write(
                        "**"
                        + field.replace(
                            "_",
                            " "
                        ).title()
                        + "**"
                    )

                    st.write(
                        "Old:",
                        values["old"]
                    )

                    st.write(
                        "New:",
                        values["new"]
                    )

            if (
                result["status"]
                != "UNCHANGED"
            ):
                explanation_key = (
                    f"explanation_{index}"
                )

                if (
                    explanation_key
                    not in st.session_state
                ):
                    if st.button(
                        "Generate AI Explanation",
                        key=f"explain_{index}"
                    ):
                        try:
                            with st.spinner(
                                "Generating explanation..."
                            ):
                                explanation = (
                                    explain_change(
                                        result
                                    )
                                )

                            st.session_state[
                                explanation_key
                            ] = explanation

                            st.rerun()

                        except Exception as error:
                            st.error(
                                "AI explanation failed: "
                                f"{error}"
                            )

                else:
                    st.markdown(
                        "### AI Explanation"
                    )

                    st.write(
                        st.session_state[
                            explanation_key
                        ]
                    )

    if visible_results == 0:
        st.info(
            "No clauses match the selected filters."
        )

    st.divider()

    st.subheader(
        "Export Comparison"
    )

    json_report = results_to_json(
        results
    )

    st.download_button(
        label="Download JSON Report",
        data=json_report,
        file_name=(
            "contract_comparison.json"
        ),
        mime="application/json",
        use_container_width=True
    )

    st.divider()

    st.subheader(
        "Ask About the Contracts"
    )

    question = st.text_input(
        "Question",
        placeholder=(
            "Example: What changed "
            "in the liability clause?"
        )
    )

    if st.button(
        "Ask AI",
        use_container_width=True
    ):
        if not question.strip():
            st.warning(
                "Enter a question first."
            )

        else:
            try:
                with st.spinner(
                    "Analyzing contracts..."
                ):
                    answer = (
                        answer_question(
                            question,
                            results
                        )
                    )

                st.markdown(
                    "### Answer"
                )

                st.write(answer)

            except Exception as error:
                st.error(
                    "AI question answering "
                    f"failed: {error}"
                )