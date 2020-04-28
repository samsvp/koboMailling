import os
import json
import smtplib
import requests
from email.message import EmailMessage
from create_pdf import create_report


def create_body(rame, result, date):
    """
    Creates the body of the email based on the result
    """

    message = f"Prezado {name},\n\nSegue em anexo o Laudo Técnico de Diagnóstico Molecular para o Vírus SARS-CoV2 de exame realizado na UFRJ no dia {date}."

    if result == "positivo": 
        message += "\nSolicitamos que retorne esse e-mail nos atualizando sobre o seu estado de saúde atual e que não hesite em contactar em caso de dúvidas. Torcemos por uma breve recuperação."
    elif result == "inconclusivo": 
        message += "\nDevido ao resultado inconclusivo, solicitamos que retorne para coleta de nova amostra, de segunda a quinta-feira, entre 8:30-11:30 da manhã, no bloco N do CCS."
    elif result == "negativo":
        pass
    else: raise Exception("Resultado inválido.", 
        "Resultado pode ser somente positivo, negativo ou inconclusivo") 

    message += "\n\nAtenciosamente, \nEquipe COVID-19 - UFRJ"
    return message


def send_email_report(to_email, body, pdf_data, pdf_name):
    """
    Sends the email to the patient and doctors informing the test results
    """
    with open('tokens.json') as f:
        data = json.load(f)

    EMAIL_ADDRESS = data["email_address"]
    EMAIL_PASS = data["email_pass"]

    msg = EmailMessage()
    msg['Subject'] = 'Resultado laboratorial Covid 19'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['CC'] = data["CC"]
    msg.set_content(body)

    msg.add_attachment(pdf_data,  maintype='application/pdf', subtype='pdf', filename=pdf_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASS)

        smtp.send_message(msg)
