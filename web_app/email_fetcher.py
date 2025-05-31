import imaplib
import email

def fetch_latest_email(email_user, email_pass):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_user, email_pass)
    mail.select("inbox")

    # Ambil 1 email terbaru
    result, data = mail.search(None, "ALL")
    email_ids = data[0].split()
    latest_id = email_ids[-1]

    result, data = mail.fetch(latest_id, "(RFC822)")
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)

    subject = msg["subject"]
    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
                break
    else:
        body = msg.get_payload(decode=True).decode()

    return subject, body
