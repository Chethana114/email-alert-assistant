def is_important_email(subject, body, has_attachment):
    subject = subject.lower()
    body = body.lower()
    text = subject + " " + body

    # ✅ Positive keywords (job/academic/professional)
    positive_keywords = [
        "job offer", "joining letter", "appointment letter", "offer letter",
        "interview", "selected", "shortlisted", "recruitment", "placement",
        "internship", "campus", "hiring", "zoom meeting", "google meet",
        "schedule", "calendar invite", "ms teams", "webex", "walk-in",
        "technical round", "confirmation", "meeting"
    ]

    # ❌ Negative spammy/shopping-related keywords
    negative_keywords = [
        "discount", "coupon", "shopping", "buy now", "deal", "sale", "myntra",
        "amazon", "flipkart", "price drop", "combo", "limited time", "exclusive deal",
        "clearance", "cosmetics", "footwear", "clothing", "apparel", "fashion", "outlet",
        "shop now", "hurry", "avail", "bargain", "festive", "cart", "store", "purchase"
    ]

    # ❌ Reject if any strong spammy/shopping word appears
    for bad in negative_keywords:
        if bad in text:
            print(f"❌ Blocked by negative keyword: {bad}")
            return False

    # ✅ Accept if a strong professional keyword appears
    for good in positive_keywords:
        if good in text:
            print(f"✅ Matched professional keyword: {good}")
            return True

    # ✅ Accept if there's an attachment and no spam
    if has_attachment:
        print("📎 Accepted because of attachment (no spam).")
        return True

    return False
