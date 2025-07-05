from core.gmail_client import fetch_unread_emails
from core.llm_classifier import classify_email_with_llm
from core.redactor import redact_email_text
from core.alert_manager import check_unread_duration
from core.storage import store_email_metadata, load_existing_ids_with_status
from core.keyword_filter import is_important_email  # ✅ Fallback + Guardrail

def run_assistant():
    existing_status = load_existing_ids_with_status()
    emails = fetch_unread_emails()

    for email in emails:
        email_id = email["id"]
        current_unread = email["unread"]
        subject = redact_email_text(email["subject"])
        body = redact_email_text(email["body"])
        has_attachment = email.get("has_attachment", False)

        print(f"📥 Processing email with ID: {email_id}")
        print(f"📌 Subject: {subject}")

        # ✅ Update only the unread status if already processed before
        if email_id in existing_status:
            print("🔄 Email already classified. Just updating unread status.")
            store_email_metadata(
                email_id=email_id,
                subject=subject,
                timestamp=email["timestamp"],
                unread=current_unread,
                alert_sent=False,
                label="important"
            )
            continue

        # === Step 1: Ask RAG model
        label = classify_email_with_llm(subject, body)
        print(f"🤖 RAG classified this email as: {label}")

        # === Step 2: Validate or fallback using keyword filter
        if label == "important":
            if not is_important_email(subject, body, has_attachment):
                print("❌ Overruled by keyword filter — spam/shopping detected.")
                label = "not important"
        else:
            print("🔄 Falling back to keyword-based check...")
            if is_important_email(subject, body, has_attachment):
                print("📌 Marked important by keyword filter fallback.")
                label = "important"

        print(f"🤖 Final Decision: '{label}'")

        # === Step 3: Store if important
        if label == "important":
            store_email_metadata(
                email_id=email_id,
                subject=subject,
                timestamp=email["timestamp"],
                unread=current_unread,
                alert_sent=False,
                label=label
            )
        else:
            print("ℹ️ Skipping email — not marked important.")

    # === Step 4: Check for alerts
    alerts = check_unread_duration(threshold_minutes=5)
    for alert in alerts:
        print(f"⚠️ ALERT: You have not seen '{alert['subject']}' in 5+ minutes!")

if __name__ == "__main__":
    run_assistant()
