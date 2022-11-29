from email.message import EmailMessage
import smtplib
import os


def send_email(to, sub):
    message = EmailMessage()
    message['subject'] = sub
    message['from'] = 'Facebook <security@facebookmail.com>'
    message['to'] = to

    # Content of email
    message.set_content(' ')
    # Open read and attached the html file to the email
    html_message = open("./scam_template/index.html").read()
    message.add_alternative(html_message,subtype='html')

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login('xxx@gmail.com','xxx')
        smtp.send_message(message)
        smtp.quit()