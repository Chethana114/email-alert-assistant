# core/scheduler.py
import time
from core.storage import get_pending_emails
from core.notifier import send_alert

def check_unread_emails():
    while True:
        pending_emails = get_pending_emails()
        for email in pending_emails:
            if email["unread_duration"] > 2 * 60:  # 2 hours in minutes
                send_alert(email["subject"])
        time.sleep(3600)  # Check every hour
