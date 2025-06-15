from embedding_util import load_chunks, load_model, embed_texts, save_embeddings

def embed_and_store_chunks(json_path: str, embedding_output_path: str):
    chunks = load_chunks(json_path)
    print(f"Loaded {len(chunks)} chunks from {json_path}")
    chunk_texts = [f"{chunk['title']} {chunk['content']}" for chunk in chunks]
    model = load_model()
    embeddings = embed_texts(model, chunk_texts)
    save_embeddings(embeddings, embedding_output_path)
    print(f"Embeddings saved to {embedding_output_path}")
