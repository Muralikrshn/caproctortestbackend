from sentence_transformers import SentenceTransformer, util
import numpy as np
import json

def load_chunks(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)  # This should be a list of text chunks

def load_model(model_name: str = 'all-MiniLM-L6-v2') -> SentenceTransformer:
    return SentenceTransformer(model_name)

def embed_texts(model: SentenceTransformer, texts: list[str], batch_size: int = 32) -> np.ndarray:
    return model.encode(texts, batch_size=batch_size, convert_to_tensor=True)

def save_embeddings(embeddings: np.ndarray, file_path: str):
    np.save(file_path, embeddings.cpu().numpy())  # Save as numpy array

def load_embeddings(file_path: str) -> np.ndarray:
    return np.load(file_path)

def cosine_similarity(query_embedding: np.ndarray, corpus_embeddings: np.ndarray) -> np.ndarray:
    return util.cos_sim(query_embedding, corpus_embeddings)[0]  # returns tensor of scores

def find_most_similar(query: str, corpus: list[str], model: SentenceTransformer, top_k: int = 1) -> list[tuple[str, float]]:
    query_emb = model.encode(query, convert_to_tensor=True)
    corpus_emb = embed_texts(model, corpus)
    scores = cosine_similarity(query_emb, corpus_emb)
    top_results = scores.topk(k=top_k)
    results = []
    for score, idx in zip(top_results.values, top_results.indices):
        results.append((corpus[idx], float(score)))
    return results



# Optional
def preprocess_text(text: str) -> str:
    # simple example
    return text.strip()
