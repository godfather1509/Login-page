import smtplib
from email.mime.text import MIMEText
import random

def sendEmail(recipients,subject):
    sender="ayush1500g@gmail.com"
    password="roml pyso volo wisr"
    body=str(random.randrange(1000000,9999999))
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")
    return body