import base64
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes: read inbox + metadata
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# ✅ Auth helper
def authenticate_gmail():
    creds = None
    token_path = 'credentials/token.json'
    creds_path = 'credentials/credentials.json'

    # Load saved credentials
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save token
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

# ✅ Fetch inbox emails + status
def fetch_unread_emails():
    service = authenticate_gmail()

    results = service.users().messages().list(
        userId="me",
        q="in:inbox -in:spam -in:trash",
        maxResults=30
        ).execute()

    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        print(f"📥 Fetching email with ID: {msg['id']}")
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()

        payload = msg_data.get("payload", {})
        headers = payload.get("headers", [])
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)")
        print(f"📌 Subject: {subject}") 
        label_ids = msg_data.get("labelIds", [])

        # ✅ Check status
        is_unread = "UNREAD" in label_ids
        body = extract_body(msg_data)
        has_attachment = check_attachments(msg_data)

        emails.append({
            "id": msg["id"],
            "subject": subject,
            "body": body,
            "timestamp": int(msg_data["internalDate"]),
            "unread": is_unread,
            "has_attachment": has_attachment,
        })

    return emails

# ✅ Extract plain text body
def extract_body(message):
    parts = message.get('payload', {}).get('parts', [])
    if not parts:
        return ""
    for part in parts:
        if part.get('mimeType') == 'text/plain':
            data = part.get('body', {}).get('data')
            if data:
                return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    return ""

# ✅ Check for attachments
def check_attachments(message):
    parts = message.get('payload', {}).get('parts', [])
    for part in parts:
        if part.get('filename') and part['filename'] != "":
            return True
    return False

