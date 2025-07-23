import json
import glob
import os
from datetime import datetime
from pdf_utils import extract_pdf_sections
from analyzer import rank_sections, model
from sklearn.metrics.pairwise import cosine_similarity

pdf_paths = sorted(glob.glob("./input_pdfs/*.pdf"))
short_pdf_names = [os.path.basename(p) for p in pdf_paths]

if not pdf_paths:
    print("No PDF files found in input_pdfs/. Please add your PDF documents there.")
    exit()

# Adjust to your scenario!
persona = "YOUR PERSONA"
job_to_be_done = "YOUR JOB TO BE DONE"

all_sections = []
for file_path, short_name in zip(pdf_paths, short_pdf_names):
    sections = extract_pdf_sections(file_path)
    print(f"{short_name}: extracted {len(sections)} sections")
    for s in sections:
        s['document'] = short_name
    all_sections.extend(sections)

if not all_sections:
    print("No sections found in any document. Adjust the extraction logic if needed.")
    output = {
        "metadata": {
            "input_documents": short_pdf_names,
            "persona": persona,
            "job_to_be_done": job_to_be_done,
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }
    with open("challenge1b_output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    exit()

ranked_sections = rank_sections(all_sections, persona, job_to_be_done)
top_sections = ranked_sections[:5] if ranked_sections else []

def extract_relevant_text(text, context):
    paras = [p.strip() for p in text.split('\n') if len(p.strip()) > 20]
    if not paras: paras = [text]
    context_vec = model.encode([context[:400]])[0]
    para_vecs = model.encode([p[:300] for p in paras])
    scores = cosine_similarity([context_vec], para_vecs)[0]
    idx = int(scores.argmax())
    return paras[idx][:500]

context = f"{persona}. {job_to_be_done}"
subsection_analysis = []
for section in top_sections:
    refined = extract_relevant_text(section['text'], context)
    subsection_analysis.append({
        "document": section['document'],
        "refined_text": refined,
        "page_number": section['page']
    })

output = {
    "metadata": {
        "input_documents": short_pdf_names,
        "persona": persona,
        "job_to_be_done": job_to_be_done,
        "processing_timestamp": datetime.now().isoformat()
    },
    "extracted_sections": [
        {
            "document": s['document'],
            "section_title": s['title'],
            "importance_rank": s['importance_rank'],
            "page_number": s['page']
        } for s in top_sections
    ],
    "subsection_analysis": subsection_analysis
}

with open("challenge1b_output.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4, ensure_ascii=False)

print("Saved output to challenge1b_output.json.")
