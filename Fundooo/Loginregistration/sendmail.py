import smtplib
import os
from django.core.mail import send_mail
from email.message import EmailMessage

def send_mail_to_recipients(mail_subject, mail_message,recipient_email):

    EMAIL_HOST  = 'smtp.gmail.com'
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_PORT = 587

   
    # smtpObj = smtplib.SMTP(EMAIL_HOST,EMAIL_PORT)
    # smtpObj.starttls()
    # smtpObj.login(EMAIL_HOST_USER,EMAIL_HOST_PASSWORD)
    # smtpObj.sendmail(EMAIL_HOST_USER, recipient_email, mail_message)         
    # print("Successfully sent email")
    # smtpObj.quit()
    # Create the container email message.
    msg = EmailMessage()
    msg['Subject'] = mail_subject
    # me == the sender's email address
    # family = the list of all recipients' email addresses
    msg['From'] = EMAIL_HOST_USER
    msg['To'] = recipient_email
    msg.preamble = 'You will not see this in a MIME-aware mail reader.'
    # Send the email via our own SMTP server.
    with smtplib.SMTP(EMAIL_HOST) as s:
        s.send_message(msg)



# Open the files in binary mode.  Use imghdr to figure out the
# MIME subtype for each specific image.









