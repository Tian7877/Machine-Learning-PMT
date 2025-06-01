import imaplib
import email

def fetch_emails(email_user, email_pass, limit=10, offset=0):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_user, email_pass)
    mail.select("inbox")

    result, data = mail.search(None, "ALL")
    email_ids = data[0].split()[::-1]  # dari terbaru
    selected_ids = email_ids[offset:offset+limit]

    emails = []
    for eid in selected_ids:
        result, data = mail.fetch(eid, "(RFC822)")
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = msg["subject"] or "(No Subject)"
        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        preview = body[:100].replace("\n", " ") + "..."
        emails.append({"subject": subject, "body": body, "preview": preview})

    return emails
