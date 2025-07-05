# core/redactor.py

import re

def redact_email_text(text: str) -> str:
    """
    Masks sensitive data in the given email text.
    """
    redacted = text

    # Redact email addresses
    redacted = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '[EMAIL]', redacted)

    # Redact phone numbers
    redacted = re.sub(r'\b\d{10}\b', '[PHONE]', redacted)

    # Redact 6-digit OTPs or codes
    redacted = re.sub(r'\b\d{6}\b', '[OTP]', redacted)

    # Redact salary / money amounts
    redacted = re.sub(r'₹?\s?\d{1,3}(?:[,.\s]?\d{3})+(?:\.\d+)?', '[AMOUNT]', redacted)

    # Redact dates (e.g., July 5, 2025 or 05/07/2025)
    redacted = re.sub(r'\b(?:\d{1,2}[/-])?\d{1,2}[/-]\d{2,4}\b', '[DATE]', redacted)
    redacted = re.sub(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}(?:,\s*\d{4})?', '[DATE]', redacted, flags=re.IGNORECASE)

    return redacted
