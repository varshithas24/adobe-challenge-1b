# Round 1B: Persona-Driven Document Intelligence

## Overview

This project is an intelligent document analyst that automatically extracts and ranks the most relevant sections from a collection of PDF documents, based on a given **persona** and **job-to-be-done**. The system is designed to be generic and robust, handling PDFs from diverse domains such as research, education, business, or any textual content.

- **Input:** 3–10 related PDF documents in `input_pdfs/`, and a persona/job-to-be-done defined in `main.py`.
- **Output:** Structured JSON (`challenge1b_output.json`) containing metadata, extracted sections, and semantic summaries.

---

## Features

- **Universal Section Extraction:** Works on any domain—scientific, business, educational, or recipe PDFs.
- **Persona-aware Relevance:** Ranks sections based on persona and specified analytical task.
- **CPU-only, Lightweight:** Model size within 1GB, and all processing is CPU-bound for compliance.
- **Containerized:** Fully reproducible via Docker; runs with a single command.

---

## File Structure

├── main.py
├── pdf_utils.py
├── analyzer.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── approach_explanation.md
├── input_pdfs/ # ← Place your PDFs here (do NOT commit large PDFs)
│ └── README.md # (explains folder use)
├── challenge1b_output.json # (created after run)


---

## How to Build and Run

### 1. **Place your input PDFs**

Put all input PDF files in the directory:
Do not commit actual PDFs to your repository—just use for local runs.

### 2. **Set Persona and Job-to-be-Done**
Edit the top of `main.py` to define your persona and task:

### 3. **Build the Docker Image**

Open a terminal/PowerShell in your project directory and run:

### 4. **Run the Pipeline**

From your project directory:
- On Windows Command Prompt, use `%cd%` instead of `${PWD}`.
- Output file (`challenge1b_output.json`) will appear in your project folder.

---

## Output

**Output file:** `challenge1b_output.json`
- Contains:
  - Metadata: document list, persona, job-to-be-done, timestamp
  - Extracted sections: document, section title, rank, page number
  - Subsection analysis: brief extract for each section

Example (see `challenge1b_output.json` for full details):


---

## Approach

See `approach_explanation.md` for methodology and pipeline details.

---

## Notes

- This repository does **not** include input PDFs for copyright reasons.
- All code is CPU-only and does not require or use GPU hardware.

---

## Contact

For any issues or clarifications, please reach out via the competition platform or your team lead.
