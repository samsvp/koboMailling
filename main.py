import tkinter as tk
from tkinter import messagebox
from threading import Thread

from get_kobo_data import get_kobo_data
from create_pdf import create_report, get_report
from mailling_system import create_body, send_email_report


data_retrieved = False
password = ""
address = ""
kobo_data = []


def send(idx, address, password):

    data = kobo_data[idx]

    sample_date = data["_submission_time"].replace("T", " ")
    result = data["identificacao/result"]
    name = data["identificacao/nm"]

    body = create_body(name, result, sample_date)

    pdf_data, pdf_name = get_report(create_report(data))

    print(address, password)

    try:
        send_email_report(address, password, "samuelsimplicio5@gmail.com", body, pdf_data, pdf_name)
    except Exception as e:
        print(e)


def show_info_box(msg):
    _ = tk.Tk()
    _.withdraw()
    messagebox.showinfo("Info", msg)
    _.destroy()


def show_error_box(msg):
    _ = tk.Tk()
    _.withdraw()
    messagebox.showerror("Error", msg)
    _.destroy()


def parse_data(window, txt_entry, txt_label):
    raw_indexs = txt_entry.get().replace(" ", "").split(",")
    
    indexes = []
    for idx in raw_indexs:
        if ":" not in idx: 
            try:
                indexes.append(int(idx))
            except ValueError as e:
                show_error_box(f"Sintaxe inválida: {e}")
                return
        else:
            try:
                begin, end = idx.split(":")            
                rng = [*range(int(begin), int(end) + 1)]
                for r in rng: indexes.append(r)
            except ValueError as e:
                show_error_box(f"Sintaxe inválida: {e}")
                return


    txt_entry.configure(state = "disabled")
    txt_label.configure(text = "Mandando emails")
    
    window.update()

    errors = []
    n_enviados = 0
    for idx in indexes:
        try:
            send(idx - 2, address, password)
            n_enviados += 1
        except KeyError as e: 
            errors.append((idx, f"dados vazios ({e})"))
        except IndexError as e:
            errors.append((idx, "nº de paciente inexistente"))
        except Exception as e:
            errors.append((idx, e))

    error_msg = "Os dados dos seguintes apresentaram erro:\n"
    for error in errors: error_msg += f"{error[0]}:  {error[1]}\n"

    if errors: show_error_box(error_msg)
    show_info_box(f"{n_enviados} emails enviados!")

    txt_entry.configure(state = "normal")
    txt_entry.delete(0, "end")
    txt_label.configure(text = "Selecione o número dos pacientes cujo laudo deve ser mandado")
    

def get_password():
    
    def _get_password(txt_user, txt_pass):
        global password, address, exit_program

        address = txt_user.get()
        password = txt_pass.get()
        destroy()


    def destroy():
        window.destroy()
        wait_data()
    

    def on_closing():
        global exit_program

        window.destroy()
        exit_program = True
        exit(0)


    window = tk.Tk()
    window.title("Kobo Email Sender")
    window.geometry('350x200')

    lbl_address = tk.Label(window, text="Digite email")
    lbl_address.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    txt_address = tk.Entry(window, width=50)
    txt_address.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    lbl_pass = tk.Label(window, text="Digite a senha para seu Roundmail")
    lbl_pass.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    txt_pass = tk.Entry(window, width=50, show="*")
    txt_pass.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    
    button = tk.Button(window, text="Log in", command=lambda: _get_password(txt_address, txt_pass))
    button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    window.bind('<Return>', lambda x: _get_password(txt_address, txt_pass))

    window.protocol("WM_DELETE_WINDOW", on_closing)

    Thread(target=get_data).start()

    window.mainloop()


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


def get_data():
    global kobo_data, data_retrieved
    
    kobo_data = get_kobo_data()
    data_retrieved = True


def main():
    global data_retrieved, kobo_data

    get_password()
    
    if not kobo_data:
        msg = "Não foi possível se conectar com o Kobo. \
Por favor, verifique sua conecção com a internet e tente novamente"
        show_error_box(msg)
        exit(0) 

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

    button = tk.Button(window, text="Enviar Emails", command=lambda: parse_data(window, txt_entry, txt_label))
    button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    window.bind('<Return>', lambda x: parse_data(window, txt_entry, txt_label))

    window.mainloop()


main()