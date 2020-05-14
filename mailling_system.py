import os
import json
import smtplib
import requests
from email.message import EmailMessage
from utils import get_file
from create_pdf import create_report


name = ""
date = ""
result = ""

def f(non_f_str: str):
    """
    f string implementation for the json variables
    """

    return eval(f'f"""{non_f_str}"""')
    

def create_body(_name, _result, _date):
    """
    Creates the body of the email based on the result
    """
    global name, date

    name = _name
    result = _result
    date = _date
    
    filename = "email_user_template.json" if os.path.isfile(get_file("email_user_template.json")) else "email_template.json"

    with open(get_file(filename), 'r', encoding='utf8') as fl:
        data = json.load(fl)

    message = f(data["corpo 1"])

    result = result.lower()

    if result == "positivo": 
        message += f(data["positivo"])
    elif result == "inconclusivo": 
        message += f(data["inconclusivo"])
    elif result == "negativo":
        message += f(data["negativo"])
    else: raise Exception("Resultado inválido.", 
        "Resultado pode ser somente positivo, negativo ou inconclusivo") 

    message += f(data["corpo 2"]) + f(data["assinatura"])
    return message


def check_login(address, password):
    """
    Verifies if the user put a valid email
    """
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(address, password)
        result = True
    except:
        result = False

    return result
    

def send_email_report(address, password, to_email, body, pdf_data, pdf_name):
    """
    Sends the email to the patient and doctors informing the test results
    """

    try:
        with open("mail_list.txt", "r") as _emails:
            emails = _emails.read()
        # transform ",", new lines and ";" into whitespace
        emails_list = emails.replace("\n"," ").replace(","," ").replace(";"," ").split(" ")
        cc = list(filter(lambda x: x!= "", emails_list)) # clean up the list
    except FileNotFoundError:
        cc = [""]

    msg = EmailMessage()
    msg['Subject'] = 'Resultado laboratorial Covid 19'
    msg['From'] = address
    msg['To'] = to_email
    msg['CC'] = cc
    msg.set_content(body)

    msg.add_attachment(pdf_data,  maintype='application/pdf', subtype='pdf', filename=pdf_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(address, password)
        smtp.send_message(msg)

