# core/storage.py

import os
import json

DATA_PATH = "data/messages.json"

def store_email_metadata(email_id, subject, timestamp, unread, alert_sent, label):
    """Store or update metadata for a processed email."""
    new_entry = {
        "id": email_id,
        "subject": subject,
        "timestamp": timestamp,
        "unread": unread,
        "alert_sent": alert_sent,
        "label": label
    }

    data = []
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print("⚠️ Warning: Corrupted JSON file. Starting fresh.")

    # Update if ID exists, else append
    found = False
    for msg in data:
        if msg["id"] == email_id:
            msg.update(new_entry)
            found = True
            break

    if not found:
        data.append(new_entry)

    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)

def load_existing_ids():
    """Return a set of all existing email IDs."""
    if not os.path.exists(DATA_PATH):
        return set()
    with open(DATA_PATH, "r") as f:
        try:
            data = json.load(f)
            return {msg["id"] for msg in data}
        except Exception:
            return set()

def load_existing_ids_with_status():
    """Return a dictionary of {email_id: unread_status} for tracking."""
    if not os.path.exists(DATA_PATH):
        return {}
    with open(DATA_PATH, "r") as f:
        try:
            data = json.load(f)
            return {msg["id"]: msg["unread"] for msg in data}
        except Exception:
            return {}
