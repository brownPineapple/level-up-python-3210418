import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print(" = = = = = = = = = = EMAIL SENDER = = = = = = = = = = ")
print("[+] Setting up the sender info")
smpt_server = 'smtp.mail.yahoo.com'
smtp_port = 465
sender_email = 'surajwandhare@yahoo.com'
load_dotenv()
password = os.getenv('E_PASSWORD')
receiver_email = 'surajwandhare96@gmail.com'

print("[+] Grabbing email data")
subject = input("Enter email subject: ")
body = input("Enter Email body:\n")

print("[+] Data accepted")
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = subject
message.attach(MIMEText(body, "plain"))

print("[+] Trying to send email")
try:
  with smtplib.SMTP_SSL(smpt_server, smtp_port) as server:
    server.login(sender_email, password)
    server.send_message(message)
    print('[*] Email sent successfully! Check your inbox')
except Exception as e:
  print(f"[-] Error sending email: {e}")