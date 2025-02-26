import smtplib
import ssl
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

# Email credentials
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
# Generate this password in your app passwords of your gmail account
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD') 
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')

def send_email(subject, body):
    """Send an email with the given subject and body."""
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))  # Use "plain" for plain text

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print("Email sent successfully to " + EMAIL_RECEIVER)
    except Exception as e:
        print("Error sending email:", e)

# Example Usage
send_email("New Jobs Today", "<h3>1. Software Engineer at Google</h3><p>Apply here: example.com</p>")