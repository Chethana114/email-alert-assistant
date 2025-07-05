# core/alert_manager.py

import time
import json
import os

DATA_PATH = "data/messages.json"

def check_unread_duration(threshold_minutes=5):  # 2 hours by default
    alerts = []
    now = int(time.time() * 1000)  # current time in ms

    if not os.path.exists(DATA_PATH):
        return alerts

    with open(DATA_PATH, "r") as f:
        messages = json.load(f)

    for msg in messages:
        if msg["unread"] and not msg["alert_sent"]:
            age_ms = now - int(msg["timestamp"])
            if age_ms > threshold_minutes * 60 * 1000:
                alerts.append(msg)

    return alerts

