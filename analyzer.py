from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def rank_sections(sections, persona, job):
    context = f"{persona}. {job}"[:400]
    context_vec = model.encode([context])[0]

    sec_texts = [((sec['title'] + " " + sec['text'])[:400] if sec['title'] and sec['text'] else "") for sec in sections]
    if sec_texts:
        sec_vecs = model.encode(sec_texts, batch_size=16, show_progress_bar=False)
        for sec, sec_vec in zip(sections, sec_vecs):
            sec['score'] = float(cosine_similarity([context_vec], [sec_vec])[0][0])
    else:
        for sec in sections:
            sec['score'] = 0.0
    ranked = sorted(sections, key=lambda s: s['score'], reverse=True)
    for idx, sec in enumerate(ranked):
        sec['importance_rank'] = idx + 1
    return ranked
