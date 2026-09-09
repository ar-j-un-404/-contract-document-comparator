# Contract & Document Comparator

An AI-assisted tool for comparing two versions of a contract or document and quickly identifying important changes.

The project detects added, removed, modified, and unchanged clauses, highlights important field changes, assigns a simple risk level, and can generate AI explanations using Ollama.

## Problem

Comparing two versions of a contract manually can be slow and error-prone.

Important changes may be easy to miss, such as:

- Payment deadlines changing
- Liability limits increasing
- Termination clauses being removed
- New data protection clauses being added
- Dates, notice periods, or obligations being modified

This project helps automate that comparison process.

## Features

- Upload and compare two PDF contracts
- Extract text from PDFs
- Clean and normalize extracted text
- Split documents into clauses
- Generate semantic embeddings
- Match similar clauses using cosine similarity
- Classify clauses as:
  - Added
  - Removed
  - Modified
  - Unchanged
- Detect important changes such as:
  - Money amounts
  - Dates
  - Notice periods
  - Obligations
- Basic risk scoring
- Side-by-side clause comparison
- Exact word-level difference highlighting
- AI-generated explanations using Ollama
- Ask questions about the compared contracts
- Filter results by status and risk
- Download comparison results as JSON
- Streamlit web interface

## Tech Stack

- Python
- Streamlit
- PyPDF
- Sentence Transformers
- Scikit-learn
- LangChain Ollama
- Ollama
- Qwen3:4B
- Regex
- Difflib

## Project Architecture

```text
Contract A + Contract B
          |
          v
    PDF Extraction
          |
          v
    Text Cleaning
          |
          v
    Clause Splitting
          |
          v
      Embeddings
          |
          v
   Semantic Matching
          |
          v
 Change Classification
          |
          v
Important Field Detection
          |
          v
     Risk Scoring
          |
          v
   AI Explanation
          |
          v
 Streamlit Interface


contract-document-comparator/
|
|-- ui.py
|-- main.py
|-- extractor.py
|-- cleaner.py
|-- chunking.py
|-- embedding.py
|-- matching.py
|-- comparator.py
|-- field_detector.py
|-- diff_utils.py
|-- exporter.py
|-- llm.py
|-- report.py
|-- requirements.txt
|-- .gitignore
