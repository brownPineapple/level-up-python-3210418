import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass

class EmailSender:
    def __init__(self):
        """Initializes the EmailSender class and prints usage instructions."""
        self.sender_email = None
        self.password = None
        self.receiver_email = None
        self.subject = None
        self.body = None
        self.smtp_server = None
        self.port = None
        self.use_tls = None
        self.print_usage()

    def print_usage(self):
        """Prints usage instructions for the EmailSender class."""
        print(
            "Welcome to EmailSender!\n"
            "Usage:\n"
            "1. Call get_user_input() to provide email credentials and SMTP details.\n"
            "2. Call construct_email(subject=None, body=None) to create an email.\n"
            "   - Optionally pass subject and body as arguments.\n"
            "3. Call send_email(message) to send the email.\n"
        )

    def get_user_input(self):
        """Collects user input for email details."""
        self.sender_email = input("Enter your email address: ")
        self.password = getpass.getpass("Enter your email password: ")  # Hides the password input
        self.receiver_email = input("Enter the receiver's email address: ")

        # Check if the sender's email is a Gmail address
        if "gmail.com" in self.sender_email.lower():
            self.smtp_server = "smtp.gmail.com"
            self.port = 587
            self.use_tls = True
            print("Gmail detected. SMTP server, port, and TLS are set automatically.")
        else:
            # Prompt user for SMTP server and port
            self.smtp_server = input("Enter the SMTP server address: ")
            self.port = int(input("Enter the SMTP server port: "))
            tls_input = input("Does the SMTP server require TLS? (yes/no): ").strip().lower()
            self.use_tls = tls_input == "yes"

    def construct_email(self, subject=None, body=None):
        """Creates and returns the email object. Optionally takes subject and body as arguments."""
        self.subject = subject or input("Enter the subject of the email: ")
        self.body = body or input("Enter the body of the email: ")

        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        message["Subject"] = self.subject
        message.attach(MIMEText(self.body, "plain"))
        return message

    def send_email(self, message):
        """Sends the constructed email using the specified SMTP server."""
        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                if self.use_tls:
                    server.starttls()  # Upgrade to secure encrypted connection
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, self.receiver_email, message.as_string())
                print("Email sent successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    email_sender = EmailSender()  # Constructor will print usage
    email_sender.get_user_input()  # Gather input from the user
    # You can pass subject and body as arguments or let the method prompt the user
    email_message = email_sender.construct_email(subject="Greetings", body="This is a test email!") 
    email_sender.send_email(email_message)  # Send the email