# Contract & Document Comparator

An AI-assisted tool that compares two versions of a contract or document and identifies important changes between them.

The system detects added, removed, modified, and unchanged clauses, highlights exact text changes, identifies important fields, assigns a basic risk level, and provides optional AI explanations using a local Ollama model.

## Problem

Comparing two versions of a contract manually can be time-consuming and error-prone.

Small but important changes can easily be missed, such as:

- Payment deadlines changing
- Liability limits increasing
- Termination clauses being removed
- New data-protection requirements being added
- Dates or notice periods changing
- Contractual obligations being modified

The Contract & Document Comparator helps automate this review process and makes important differences easier to identify.

## Features

- Upload and compare two PDF contracts
- Extract text from PDFs
- Clean and normalize extracted text
- Split documents into individual clauses
- Generate semantic embeddings for clauses
- Match similar clauses using cosine similarity
- Classify clauses as:
  - Added
  - Removed
  - Modified
  - Unchanged
- Detect important changes such as:
  - Monetary values
  - Dates
  - Notice periods
  - Obligations
- Rule-based risk scoring
- Side-by-side contract comparison
- Word-level difference highlighting
- Filter clauses by status and risk
- AI-generated explanations using Ollama
- Ask questions about the compared contracts
- Download comparison results as JSON
- Streamlit web interface
- CLI version

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

## Architecture

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
   Streamlit UI
```

## Project Structure

```text
contract-document-comparator/
│
├── ui.py
├── main.py
├── extractor.py
├── cleaner.py
├── chunking.py
├── embedding.py
├── matching.py
├── comparator.py
├── field_detector.py
├── diff_utils.py
├── exporter.py
├── llm.py
├── report.py
├── requirements.txt
└── .gitignore
```

## How It Works

### 1. PDF Extraction

The uploaded PDF files are read using PyPDF.

Text is extracted from every page and combined into a single document string.

### 2. Text Cleaning

The extracted text is normalized by removing unnecessary spaces and tabs while preserving useful document structure.

### 3. Clause Splitting

Regular expressions are used to identify numbered sections such as:

```text
1. Payment Terms
2. Termination
3. Confidentiality
```

Each section is stored as an individual clause.

### 4. Semantic Embeddings

Each clause is converted into a semantic vector using:

```text
all-MiniLM-L6-v2
```

from Sentence Transformers.

This allows clauses to be compared based on meaning rather than only exact words.

### 5. Clause Matching

Cosine similarity is calculated between clauses from Contract A and Contract B.

The system attempts to find the most semantically similar clause between the two documents.

### 6. Change Classification

Clauses are classified as:

```text
UNCHANGED
MODIFIED
ADDED
REMOVED
```

### 7. Important Field Detection

Regex-based detectors identify changes involving:

- Money
- Dates
- Notice periods
- Contractual obligations

For example:

```text
USD 10,000 -> USD 50,000
```

### 8. Risk Scoring

A rule-based scoring system assigns each detected change one of three levels:

```text
LOW
MEDIUM
HIGH
```

The score considers factors such as:

- Type of change
- Monetary changes
- Notice-period changes
- Obligation changes
- Important keywords such as liability, termination and payment

The risk score is intended only as a review aid and not as a legal assessment.

### 9. Word-Level Difference Highlighting

Modified clauses are compared using Python's `difflib`.

For example:

```text
Contract A:
Payment shall be made within [30] days.

Contract B:
Payment shall be made within [15] days.
```

This makes small changes easier to notice.

### 10. AI Explanation

Changed clauses can optionally be sent to a local Ollama model.

The AI explains:

1. What changed
2. Why the change may matter
3. What should be reviewed carefully

The current model is:

```text
qwen3:4b
```

AI explanations are generated only when requested instead of automatically for every clause.

### 11. Contract Q&A

Users can ask questions such as:

```text
What changed in the liability clause?
```

The local language model answers using the contract comparison as context.

### 12. Streamlit Interface

The Streamlit UI provides:

- PDF upload
- Comparison summary
- Modified-clause count
- Added-clause count
- Removed-clause count
- Unchanged-clause count
- High-risk change count
- Status filters
- Risk filters
- Side-by-side comparison
- Exact change highlighting
- AI explanations
- Contract Q&A
- JSON report download

## Installation

Clone the repository:

```bash
git clone https://github.com/ar-j-un-404/-contract-document-comparator.git
```

Move into the project:

```bash
cd -contract-document-comparator
```

Create a virtual environment:

```bash
python -m venv .venv
```

### Activate on Windows Command Prompt

```bash
.venv\Scripts\activate
```

### Activate on Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Requirements

The project uses:

```text
pypdf
sentence-transformers
scikit-learn
langchain-ollama
streamlit
```

## Ollama Setup

Install Ollama and download the model:

```bash
ollama pull qwen3:4b
```

Make sure Ollama is running before using AI explanations or contract Q&A.

## Run the Web Application

Start Streamlit:

```bash
streamlit run ui.py
```

Streamlit will display a local URL in the terminal.

Open that URL in your browser and upload two contracts.

## Run the CLI Version

The project also contains a command-line version:

```bash
python main.py
```

Enter the paths of Contract A and Contract B when prompted.

## Example

### Contract A

```text
1. Payment Terms
Payment must be made within 30 days.

2. Liability
Maximum liability is USD 10,000.
```

### Contract B

```text
1. Payment Terms
Payment must be made within 15 days.

2. Liability
Maximum liability is USD 50,000.

3. Data Protection
The service provider must protect personal data.
```

### Detected Changes

```text
Payment Terms
MODIFIED
30 days -> 15 days

Liability
MODIFIED
USD 10,000 -> USD 50,000

Data Protection
ADDED
```

## Real-World Use Cases

The project demonstrates how automated document comparison can assist with:

- Vendor agreement comparison
- Business contracts
- Employment agreement revisions
- Freelancer-client contracts
- Privacy policy updates
- Terms and conditions changes
- Internal company policy comparison
- Document version review

## Current Limitations

This is currently an educational and portfolio project.

Some limitations are:

- Designed primarily for text-based PDFs
- Scanned PDFs currently require OCR support
- Clause detection works best with numbered sections
- Semantic matching can occasionally pair unrelated clauses
- Risk scoring is rule-based
- Important-field detection is regex-based
- AI explanations depend on the local Ollama model
- Large contracts may require more advanced retrieval techniques
- It does not determine whether a contract is legally valid or acceptable

## Future Improvements

Planned improvements include:

- DOCX support
- OCR support for scanned PDFs
- Improved clause-title matching
- More advanced semantic matching
- Better payment deadline detection
- Percentage and penalty detection
- Party-name extraction
- More advanced obligation detection
- PDF report export
- Contract-level summaries
- Improved support for large documents

## Disclaimer

This project is designed for document comparison, educational use and AI experimentation.

It does not provide legal advice and should not be used as a replacement for professional legal review.

## Author

**Arjun B**

GitHub: https://github.com/ar-j-un-404
