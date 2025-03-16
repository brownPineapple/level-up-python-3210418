import smtplib
from getpass import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print(" = = = = = = = = = = EMAIL SENDER = = = = = = = = = = ")
print("[+] Setting up the sender info")
sender_email = input("Sender Email Address: ")
password = getpass()
receiver_email = input("Receiver Email Address: ")

print("[+] Enter Email Data")
subject = input("Enter Email Subject: ")
body = input("Enter Email Body:\n")

print("[+] Data Accepted")
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = subject
message.attach(MIMEText(body, "plain"))

print("[+] Trying to send email")
try:
  with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login(sender_email, password)
    server.send_message(message)
    print('[*] Email sent successfully! Check your inbox')
except Exception as e:
  print(f"[-] Error sending email: {e}")