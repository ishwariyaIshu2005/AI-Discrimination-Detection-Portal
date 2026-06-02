import smtplib
from email.mime.text import MIMEText

def send_email(
    sender_email,
    sender_password,
    receiver_email,
    message
):

    try:

        msg = MIMEText(message)

        msg["Subject"] = "AI Alert"

        msg["From"] = sender_email

        msg["To"] = receiver_email

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            sender_email,
            sender_password
        )

        server.send_message(msg)

        server.quit()

        return True

    except:

        return False