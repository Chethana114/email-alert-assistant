# core/llm_classifier.py

import os
os.environ["TRANSFORMERS_NO_TF"] = "1"  # ✅ Force PyTorch-only mode

from core.redactor import redact_email_text
from rag_engine.rag_pipeline import is_email_important

def classify_email_with_llm(subject, body):
    subject = redact_email_text(subject)
    body = redact_email_text(body)

    print("🤖 Asking RAG if this email is important...")
    important = is_email_important(subject, body)

    label = "important" if important else "not important"
    print(f"✅ RAG classified this email as: {label}")

    return label
