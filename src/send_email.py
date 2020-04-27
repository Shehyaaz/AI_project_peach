# import necessary packages
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from data import sender_email
# email template
template = '''Dear {0},\n\n{1}\n\nYours Truly,\nPeach'''

def send_mail(name,email, content):
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(sender_email[0], sender_email[1])

    msg = MIMEMultipart()  # create a message
    # add in the actual person name to the message template
    message = template.format(name,content)
    # setup the parameters of the message
    msg['From'] = sender_email[0]
    msg['To'] = email
    msg['Subject'] = "From Peach"

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # send the message via the server set up earlier.
    mail.send_message(msg)
    del msg