import tkinter as tk 
from threading import Thread

from get_kobo_data import get_kobo_data
from create_pdf import create_report, get_report
from mailling_system import create_body, send_email_report

data_retrieved = False
kobo_data = []


def send(idx):
    data = kobo_data[idx]

    sample_date = data["_submission_time"].replace("T", " ")
    result = data["identificacao/result"]

    body = create_body(result, sample_date)

    pdf_data, pdf_name = get_report(create_report(data))

    #send_email_report("samuelsimplicio5@gmail.com", body, pdf_data, pdf_name)


def parse_data(txt_entry, txt_label):
    raw_indexs = txt_entry.get().replace(" ", "").split(",")
    
    indexes = []
    for idx in raw_indexs:
        if ":" not in idx: indexes.append(int(idx))
        else:
            begin, end = idx.split(":")
            rng = [*range(int(begin), int(end) + 1)]
            for r in rng: indexes.append(r)

    print(indexes)
    
    txt_entry.configure(state = "disabled")
    txt_label.configure(text = "Mandando emails")

    for idx in indexes: send(idx)
    
    txt_entry.delete(0, "end")
    txt_entry.configure(state = "normal")
    txt_label.configure(text = "Selecione o número dos pacientes cujo laudo deve ser mandado")
    

def wait_data():

    def destroy():
        if data_retrieved: window.destroy()
        else: window.after(100, destroy)
    
    window = tk.Tk()
    window.title("Kobo Email Sender")
    window.geometry('350x200')

    txt_label = tk.Label(window, text="Carregando dados do Kobo")
    txt_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    window.after(100, destroy)
    
    window.mainloop()


def main():
    global data_retrieved, kobo_data

    Thread(target=wait_data).start()
    
    kobo_data = get_kobo_data()
    
    data_retrieved = True

    window = tk.Tk()
    window.title("Kobo Email Sender")
    window.geometry('680x400')

    exp_label2 = tk.Label(window, text="Para selecionar pacientes dentro de um intervalos utilize dois ponto ':' e.g.\n \
         o input 500:600, 700, 800 irá selecionar todos os pacientes entre 500 e 600 e os pacientes de nº 700 e 800.")
    exp_label2.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    exp_label1 = tk.Label(window, text="Separe os números por vírgula.")
    exp_label1.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    txt_label = tk.Label(window, text="Selecione o número dos pacientes cujo laudo deve ser mandado")
    txt_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    txt_entry = tk.Entry(window, width=50)
    txt_entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    button = tk.Button(window, text="Enviar Emails", command= lambda: parse_data(txt_entry, txt_label))
    button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    window.mainloop()


# kobo_data = get_kobo_data()

# sample_date = kobo_data["_submission_time"].replace("T", " ")
# result = kobo_data["identificacao/result"]

# body = create_body(result, sample_date)

# pdf_data, pdf_name = get_report(create_report(kobo_data))

# send_email_report("samuelsimplicio5@gmail.com", body, pdf_data, pdf_name)

main()