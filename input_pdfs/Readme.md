# input_pdfs/

This folder is for **input PDF documents** that you want to analyze with the document intelligence pipeline.

## Instructions:

1. Put 3–10 related PDF files for your test case or scenario in this folder.
2. Example documents:
    - Research papers (for academic persona)
    - Annual reports (for business persona)
    - Textbook chapters (for student persona)
    - News articles, recipes, etc. (for any domain)
3. **Do not commit or upload actual PDFs to the repository.**  
   Only add them here locally for your own runs.

When the pipeline runs (via `main.py` or Docker), it will automatically analyze all PDFs found in this directory.
