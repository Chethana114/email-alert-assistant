# rag_engine/vector_store.py

import os
import json
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
from chromadb.utils import embedding_functions


# === 1. Load embedding model ===
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
sentence_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL_NAME)


# === 2. Setup ChromaDB ===
CHROMA_DB_DIR = "rag_engine/chroma_store"
COLLECTION_NAME = "emails"

# ✅ Use new PersistentClient (Chroma v1.0+)
chroma_client = PersistentClient(path=CHROMA_DB_DIR)
collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=sentence_ef)


# === 3. Load and preprocess emails ===
def load_email_data(json_path="data/sample_emails.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


# === 4. Add emails to vector DB ===
def populate_vector_store():
    emails = load_email_data()
    documents = []
    ids = []
    metadata = []

    for idx, email in enumerate(emails):
        doc_text = f"Subject: {email.get('subject', '')}\n\n{email.get('body', '')}"
        documents.append(doc_text)
        ids.append(f"email_{idx}")
        metadata.append({
            "from": email.get("from") or "unknown",
            "to": email.get("to") or "unknown",
            "subject": email.get("subject") or "unknown"
        })

    # Add to ChromaDB (skip existing)
    existing_ids = collection.get(include=[])["ids"]
    new_ids = [id_ for id_ in ids if id_ not in existing_ids]

    if new_ids:
        new_docs = [documents[i] for i, id_ in enumerate(ids) if id_ in new_ids]
        new_meta = [metadata[i] for i, id_ in enumerate(ids) if id_ in new_ids]

        collection.add(
            documents=new_docs,
            metadatas=new_meta,
            ids=new_ids
        )
        print(f"✅ Added {len(new_docs)} new emails to vector store.")
    else:
        print("✅ No new emails to add")

# === 5. Query top-k similar chunks ===
def query_similar_emails(query_text, top_k=3):
    results = collection.query(
        query_texts=[query_text],
        n_results=top_k
    )

    top_docs = results['documents'][0]
    top_metas = results['metadatas'][0]
    return list(zip(top_docs, top_metas))


# === Main ===
if __name__ == "__main__":
    populate_vector_store()

    # Test with a query
    query = "Job offer from Infosys"
    results = query_similar_emails(query)

    print("\n📌 Top Matching Emails:")
    for doc, meta in results:
        print(f"\n---\n📨 Subject: {meta['subject']}\n{doc[:300]}...")
