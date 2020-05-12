import os
import sys
import json
from threading import Thread
import GUI
from utils import get_file
from get_kobo_data import get_kobo_data
from create_pdf import create_report, get_report
from mailling_system import create_body, send_email_report, check_login


data_retrieved = False
password = ""
address = ""
kobo_data = []


def _send(idx, pdf_template_data):
    """
    Sends an email to the patient containing the test result and a report.
    """
    _kobo_data = kobo_data[idx]

    to_email = _kobo_data["identificacao/eml"]

    sample_date = _kobo_data["_submission_time"].replace("T", " ")
    result = _kobo_data["identificacao/result"]
    name = _kobo_data["identificacao/nm"]

    body = create_body(name, result, sample_date)

    pdf_data, pdf_name = get_report(create_report(_kobo_data, pdf_template_data))

    send_email_report(address, password, to_email, body, pdf_data, pdf_name)


def send(indexes):
    """
    Sends an email to all the patient containing the test result and a report in the
    indexes list.
    """
    
    filename = "pdf_user_template.json" if os.path.isfile(get_file("pdf_user_template.json")) else "pdf_template.json"

    with open(get_file(filename), 'r', encoding='utf8') as fl:
        pdf_template_data = json.load(fl)

    errors = []
    n_enviados = 0
    for idx in indexes:
        try:
            # Due to excel spreadsheets number, every patient number has an offset of 2
            _send(idx - 2, pdf_template_data)
            n_enviados += 1
        except KeyError as e: 
            errors.append((idx, f"dados vazios ({e})"))
        except IndexError as e:
            errors.append((idx, "nº de paciente inexistente"))
        except Exception as e:
            errors.append((idx, e))

    error_msg = "Os dados dos seguintes apresentaram erro:\n"
    for error in errors: error_msg += f"{error[0]}:  {error[1]}\n"

    if errors: GUI.show_error_box(error_msg)
    GUI.show_info_box(f"{n_enviados} emails enviados!")

    GUI.refresh_trigger = True


def parse_data(window, txt_entry, txt_label):
    """
    Parse the data from the text box to get the numbers of the patients
    which we wish to send an email to.
    """
    raw_indexs = txt_entry.get().replace(" ", "").split(",")
    
    indexes = []
    for idx in raw_indexs:
        if ":" not in idx: 
            try:
                indexes.append(int(idx))
            except ValueError as e:
                GUI.show_error_box(f"Sintaxe inválida: {e}")
                return
        else:
            try:
                begin, end = idx.split(":")            
                rng = [*range(int(begin), int(end) + 1)]
                for r in rng: indexes.append(r)
            except ValueError as e:
                GUI.show_error_box(f"Sintaxe inválida: {e}")
                return

    GUI.sending_emails_trigger = True
    GUI.show_info_box(f"Mandando {len(indexes)} emails")

    send(indexes)
    

def get_data():
    global kobo_data, data_retrieved
    
    kobo_data = get_kobo_data()
    data_retrieved = True
    GUI.data_retrieved = True


def main():
    global data_retrieved, kobo_data, address, password

    Thread(target=get_data).start()

    credentials = []
    GUI.get_credentials(credentials)
    address, password = credentials

    if not kobo_data:
        msg = "Não foi possível se conectar com o Kobo. \
Por favor, verifique sua conecção com a internet e tente novamente"
        GUI.show_error_box(msg)
        sys.exit(0) 

    GUI.main_window(parse_data)


main()