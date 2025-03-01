import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os



def send_verification_email(to_email, verification_link):
    # SMTP server configuration (For Gmail)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = os.environ["SENDER_EMAIL"] # Replace with your email
    sender_password = os.environ["SENDER_PWD"] # use an App Password if you have 2FA enabled

    # Compose the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = 'Please verify your email address'

    # Email body
    body = f'Hello {to_email},\n\nWelcome to dentagen. \n\n Please click on the following link to verify your email address:\n\n{verification_link}\n\nThank you!'
    message.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send the email
    try:
        # Set up the SMTP server connection
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Encrypts the email
        server.login(sender_email, sender_password)
        text = message.as_string()
        
        # Send the email
        server.sendmail(sender_email, to_email, text)
        print(f"Verification email sent successfully to {to_email}!")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        server.quit()

# Example usage
verification_link = "http://127.0.0.1:8000/"  
to_email = "schiyonko@gmail.com"  # Replace with the user's email address
send_verification_email(to_email, verification_link)
