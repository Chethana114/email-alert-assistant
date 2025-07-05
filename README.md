# 📬 Email Alert Assistant

A smart assistant that scans your Gmail inbox for unread emails, classifies them using RAG-based LLMs, and displays important alerts (like offer letters, joining letters, or meeting invites) on a real-time Streamlit dashboard.

---

## 🚀 Features

- 🔁 Periodic email scanning via cron scheduler
- 🤖 LLM-based classification using **google/flan-t5-base** + **Retrieval-Augmented Generation (RAG)**
- 🔍 Keyword fallback mechanism for robust classification
- 📩 Alerts for offer letters, joining letters, meetings, or emails with attachments
- 🧠 Vector search using **ChromaDB** and **SentenceTransformer (all-MiniLM-L6-v2)**
- 🔒 Redacts sensitive info before LLM processing
- 📊 Real-time display using **Streamlit Dashboard**
- 💬 Logs classification output with timestamps

---

## 🛠️ Tech Stack

| Category            | Tools Used                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| Backend             | Python, Gmail API, Cron, Regex                                              |
| Machine Learning    | Hugging Face Transformers, FLAN-T5, SentenceTransformers                   |
| Vector Search       | ChromaDB, Cosine Similarity                                                 |
| Frontend            | Streamlit                                                                  |
| Data Storage        | JSON, SQLite                                                                |
| Other               | FFmpeg (used in related project), Git, VS Code                             |

---

## 📁 Project Structure

```bash
email_alert_assistant/
├── background_runner.py          # Entry point - triggers periodic processing
├── main.py                       # Core assistant runner
├── core/
│   ├── gmail_client.py           # Gmail API auth + fetch unread emails
│   ├── llm_classifier.py         # RAG-based classification using FLAN-T5
│   ├── keyword_filter.py         # Backup keyword-based classification
│   ├── redactor.py               # Redacts sensitive info before LLM use
│   ├── alert_manager.py          # Alert triggering and logic
│   ├── notifier.py               # Logging and output
│   ├── scheduler.py              # Cron-based periodic checks
│   └── storage.py                # Load/save message cache
├── dashboard/dashboard.py        # Streamlit frontend
├── rag_engine/                   # Vector DB & embedding logic
│   ├── chroma_store/
│   ├── rag_pipeline.py
│   └── vector_store.py
├── data/                         # Sample data and message logs
├── requirements.txt
└── README.md
