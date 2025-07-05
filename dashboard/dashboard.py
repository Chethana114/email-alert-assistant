


import streamlit as st
import json
import os
import sys
from datetime import datetime
from streamlit_autorefresh import st_autorefresh  # ⬅️ NEW

# ✅ Add root directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.alert_manager import check_unread_duration

# ✅ Auto-refresh every 15 minutes
st_autorefresh(interval=900000, key="auto_refresh")  # 900000ms = 15s mins

st.set_page_config(page_title="Email Alert Assistant", page_icon="📬")
st.title("📬 Email Alert Assistant Dashboard")

data_path = "data/messages.json"

# === ALERT SECTION ===
st.subheader("⚠️ Unread Alerts")
alerts = check_unread_duration(threshold_minutes=5)

if alerts:
    for alert in alerts:
        st.error(f"⚠️ You haven’t seen '{alert['subject']}' in 5+ minutes!")
else:
    st.success("✅ No pending alerts. You're all caught up!")

st.markdown("---")

# === EMAIL LISTING SECTION ===
st.subheader("📩 Tracked Important Emails")

if not os.path.exists(data_path):
    st.warning("messages.json not found.")
else:
    with open(data_path, "r") as f:
        try:
            messages = json.load(f)
        except json.JSONDecodeError:
            st.error("⚠️ Could not load messages.json (invalid format).")
            messages = []

    if messages:
        # === Search and Filter Controls ===
        # === Search Control Only ===
        st.text_input("🔍 Search by Subject", key="subject_search")
        subject_search = st.session_state.subject_search.lower()

        # === Apply Search Filter Only ===
        filtered_messages = []
        for msg in messages:
            subject = msg.get("subject", "").lower()

            if subject_search and subject_search not in subject:
                continue

            filtered_messages.append(msg)


        # === Display Results ===
        if filtered_messages:
            for msg in sorted(filtered_messages, key=lambda x: x['timestamp'], reverse=True):
                st.write(f"📧 **Subject:** {msg['subject']}")
                st.write(f"🏷️ **RAG Label:** {msg.get('label', 'N/A')}")

                ts = int(msg['timestamp']) // 1000
                readable_time = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
                st.write(f"🕒 **Time:** {readable_time}")

                status = "✅ Read" if not msg["unread"] else "📭 Unread"
                st.write(f"📌 **Status:** {status}")
                st.write(f"🆔 **Message ID:** `{msg['id']}`")
                st.markdown("---")
        else:
            st.info("No emails matched your filter/search.")
    else:
        st.info("No tracked emails found.")
