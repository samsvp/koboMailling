import os
import smtplib
import requests
import pdfkit as pdf
from email.message import EmailMessage

def send_email_report(to_email, message):
    EMAIL_ADDRESS = 'email@mail.com'
    EMAIL_PASS = 'email-pass'

    msg = EmailMessage()
    msg['Subject'] = 'Resultado laboratorial Covid 19'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content(message)

    pdf.from_file("laudo_sars_cov.html", "laudo_covid-19.pdf")

    with open('laudo_covid-19.pdf', 'rb') as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(file_data,  maintype='application/pdf', subtype='pdf', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASS)

        smtp.send_message(msg)
