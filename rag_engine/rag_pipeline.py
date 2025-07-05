# rag_engine/rag_pipeline.py

import sys
import os
os.environ["TRANSFORMERS_NO_TF"] = "1"  # ✅ Disable TensorFlow

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from transformers import pipeline
from rag_engine.vector_store import query_similar_emails

# === 1. Load the generative LLM ===
rag_llm = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    tokenizer="google/flan-t5-base"
)

# === 2. Build the prompt with instruction
def build_prompt(query, retrieved_docs):
    context = "\n\n".join([doc for doc, _ in retrieved_docs])
    prompt = f"""
You are a helpful email assistant.

Your task is to decide whether the following email is **important** based on its content.

An email is considered **important** ONLY if it is about:
- Job offers
- Joining letters
- Interviews
- Internship confirmations
- Task assignments
- Project meetings
- HR or career communication

Emails related to promotions, discounts, advertisements, marketing, or spam are **not important**.

Based on the context below, answer the user's question.

Context:
{context}

Question: {query}
Answer:"""
    return prompt

# === 3. General-purpose RAG response
def generate_rag_response(user_query, top_k=3):
    retrieved = query_similar_emails(user_query, top_k=top_k)
    if not retrieved:
        return "No relevant information found."

    prompt = build_prompt(user_query, retrieved)
    result = rag_llm(prompt, max_length=256, do_sample=True, temperature=0.7)
    return result[0]["generated_text"]

# === 4. Classification via RAG
def is_email_important(subject, body):
    full_text = f"Subject: {subject}\n\n{body}"
    retrieved = query_similar_emails(full_text, top_k=3)
    prompt = build_prompt("Is this email important? Reply yes or no.", retrieved)
    result = rag_llm(prompt, max_length=10, do_sample=False)[0]["generated_text"].strip().lower()
    return "yes" in result

# === Main test
if __name__ == "__main__":
    test_query = "What is this email about?"
    response = generate_rag_response(test_query)
    print("\n🤖 RAG Answer:\n", response)
