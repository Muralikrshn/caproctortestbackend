from embedding_util import load_chunks, load_model, load_embeddings, cosine_similarity

def run_query(user_query: str, json_path: str, embedding_path: str, top_k: int = 3):
  chunks = load_chunks(json_path)
  chunk_texts = [f"{chunk['title']} {chunk['content']}" for chunk in chunks]
  model = load_model()
  embeddings = load_embeddings(embedding_path)

  query_emb = model.encode(user_query, convert_to_tensor=True)
  scores = cosine_similarity(query_emb, embeddings)
  top_results = scores.topk(k=top_k)

  retrieved_contexts = []
  # print(f"\nTop {top_k} results for: \"{user_query}\"\n")
  for score, idx in zip(top_results.values, top_results.indices):
    context = chunk_texts[int(idx)]
    retrieved_contexts.append(context)
    # print(f"\n--- Score: {float(score):.4f} ---\n")
    # print(chunk_texts[int(idx)])
    # print("\n---------------------------\n")

  combined_context = "\n\n".join(retrieved_contexts)
  return combined_context
