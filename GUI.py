import os
import sys
import json
import subprocess
from utils import get_file
from create_pdf import create_report
from mailling_system import create_body, send_email_report, check_login

try:
    import tkinter as tk
    from tkinter import messagebox
except: # Rename lib/Tkinter folder made by cv_Freeze executable
    exe_dir = os.path.dirname(sys.executable)
    os.rename(os.path.join(exe_dir, "lib","Tkinter"), os.path.join(exe_dir, "lib","tkinter"))
    import tkinter as tk
    from tkinter import messagebox


data_retrieved = False
sending_emails_trigger = False
refresh_trigger = False


# Every messagebox must belong to a window, so we create a 
# window, hide it, and destroy when the box is closed.
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


def wait_data():
    """
    Wait for kobo to retrieve data
    """
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


def get_credentials(credentials):
    """
    Get user credentials
    """
    def _get_credentials(txt_user, txt_pass):
        address = txt_user.get()
        password = txt_pass.get()
        
        if "@" not in address: address += "@gmail.com"

        if check_login(address, password): 
            credentials.append(address)
            credentials.append(password)
            destroy()
        else: 
            msg = """
                Não foi possível realizar login no email.
                Por favor verifique se o usuário e senha estão corretos e sua conexão com a internet.
                """
            show_error_box(msg)


    def destroy():
        window.destroy()
        wait_data()
    

    def on_closing():
        global exit_program

        window.destroy()
        exit_program = True
        sys.exit(0)


    window = tk.Tk()
    window.title("Kobo Email Sender")
    window.geometry('350x200')

    lbl_address = tk.Label(window, text="Digite email")
    lbl_address.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    txt_address = tk.Entry(window, width=50)
    txt_address.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    lbl_pass = tk.Label(window, text="Senha")
    lbl_pass.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    txt_pass = tk.Entry(window, width=50, show="*")
    txt_pass.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    
    button = tk.Button(window, text="Log in", command=lambda: _get_credentials(txt_address, txt_pass))
    button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    window.bind('<Return>', lambda x: _get_credentials(txt_address, txt_pass))

    window.protocol("WM_DELETE_WINDOW", on_closing)

    window.mainloop()


def pdf_help():
    window = tk.Tk()
    window.title("Ajuda: Editor de PDF")
    window.geometry('700x500')

    text = """
Digite nos campos possíveis as modificações desejadas no template de pdf.

Aperte o botão "Visualizar" para poder visualizar o pdf conforme os dados inserido.
Aperte o botão "Reset" para desfazer as alterações.
Aperte o botão "Salvar" para salvar suas alterações.
Aperte o botão "Default" e aperte salvar para utilizar o template padrão.
As alterações feitas não serão salvas caso se feche a janela do editor de PDF sem apertar o botão "Salvar".

As seguintes variáveis podem ser inseridas no pdf escrevendo-as entre chaves ({ }):

paciente = "{paciente}"
data de coleta da amostra = "{data_amostra}"
ID do paciente = "{ID}"
resultado = "{resultado}"
Horário atual = "{dt}"

O sumário com os dados do paciente no topo do documento não pode ser alterado.
    """

    lbl = tk.Label(window, text=text, font=("Arial", 10, "bold"), wraplength=500)
    lbl.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    lbl.pack()

    window.mainloop()


def _edit_pdf(window, data):
    
    def save():
        """
        Saves the user changes.
        """
        data["Fonte_Título"] = txt_font_title.get("1.0",'end-1c')
        data["Fonte_Título_tamanho"] = int(txt_font_title_size.get("1.0",'end-1c'))
        data["Fonte"] = body_font.get("1.0",'end-1c')
        data["Fonte_tamanho"] = int(body_font_size.get("1.0",'end-1c'))
        data["Título"] = txt_title.get("1.0",'end-1c')
        data["Assinatura"] = txt_ass.get("1.0",'end-1c')
        data["Metodologia"] = txt_methodology.get("1.0",'end-1c')
        data["Resultado"] = txt_result.get("1.0",'end-1c')
        data["Conclusão"] = txt_conclusion.get("1.0",'end-1c')
        data["Observações"] = txt_obs.get("1.0",'end-1c')

        with open(get_file("pdf_user_template.json"), "w", encoding='utf8') as fl:
            json.dump(data, fl, ensure_ascii=False, indent=0)

        show_info_box("Dados salvos!")

    def preview():
        """
        Allows the user to preview the changes he made.
        """
        _data = {}
        _data["Fonte_Título"] = txt_font_title.get("1.0",'end-1c')
        _data["Fonte_Título_tamanho"] = int(txt_font_title_size.get("1.0",'end-1c'))
        _data["Fonte"] = body_font.get("1.0",'end-1c')
        _data["Fonte_tamanho"] = int(body_font_size.get("1.0",'end-1c'))
        _data["Título"] = txt_title.get("1.0",'end-1c')
        _data["Assinatura"] = txt_ass.get("1.0",'end-1c')
        _data["Metodologia"] = txt_methodology.get("1.0",'end-1c')
        _data["Resultado"] = txt_result.get("1.0",'end-1c')
        _data["Conclusão"] = txt_conclusion.get("1.0",'end-1c')
        _data["Observações"] = txt_obs.get("1.0",'end-1c')
        print(_data)

        _kobo_data = {"identificacao/nm": "{nome}", "_submission_time": "{_submission_time}", 
                      "identificacao/result": "{resultado}", "_id": "{id}"}
        
        show_info_box("Por favor, aguarde enquanto abrimos o seu PDF")

        create_report(_kobo_data, _data, "preview.pdf")
        try:
            subprocess.Popen("preview.pdf", shell=True)
        except Exception as e:
            show_error_box(e)

    def default():
        with open(get_file("pdf_template.json"), 'r', encoding='utf8') as fl:
            data = json.load(fl)
        
        _edit_pdf(window, data)

    def reset():
        filename = "pdf_user_template.json" if os.path.isfile(get_file("pdf_user_template.json")) else "pdf_template.json"

        with open(get_file(filename), 'r', encoding='utf8') as fl:
            data = json.load(fl)
        
        _edit_pdf(window, data)


    title = tk.Label(window, text="Editor do template de PDF", font=("Arial", 15, "bold"))
    title.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

    title = tk.Label(window, text="Título")
    title.place(relx=0.35, rely=0.1, anchor=tk.W)

    txt_title = tk.Text(window, height=1, width=60)
    txt_title.place(relx=0.05, rely=0.15, anchor=tk.W)
    txt_title.insert(tk.INSERT, data["Título"])

    title_font = tk.Label(window, text="Fonte")
    title_font.place(relx=0.74, rely=0.1, anchor=tk.E)

    txt_font_title = tk.Text(window, height=1, width=10)
    txt_font_title.place(relx=0.8, rely=0.15, anchor=tk.E)
    txt_font_title.insert(tk.INSERT, data["Fonte_Título"])

    title_font_size = tk.Label(window, text="Tamanho da fonte")
    title_font_size.place(relx=0.95, rely=0.1, anchor=tk.E)

    txt_font_title_size = tk.Text(window, height=1, width=10)
    txt_font_title_size.place(relx=0.95, rely=0.15, anchor=tk.E)
    txt_font_title_size.insert(tk.INSERT, data["Fonte_Título_tamanho"])

    txt_corpo = tk.Label(window, text="Corpo")
    txt_corpo.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    font = tk.Label(window, text="Fonte")
    font.place(relx=0.3, rely=0.25, anchor=tk.CENTER)
    
    body_font = tk.Text(window, height=1, width=10)
    body_font.place(relx=0.3, rely=0.3, anchor=tk.CENTER)
    body_font.insert(tk.INSERT, data["Fonte"])

    font_size = tk.Label(window, text="Tamanho da fonte")
    font_size.place(relx=0.7, rely=0.25, anchor=tk.CENTER)
    
    body_font_size = tk.Text(window, height=1, width=10)
    body_font_size.place(relx=0.7, rely=0.3, anchor=tk.CENTER)
    body_font_size.insert(tk.INSERT, data["Fonte_tamanho"])

    methodology = tk.Label(window, text="Metodologia")
    methodology.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

    txt_methodology = tk.Text(window, height=3, width=80)
    txt_methodology.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    txt_methodology.insert(tk.INSERT, data["Metodologia"])

    result = tk.Label(window, text="Resultado")
    result.place(relx=0.5, rely=0.47, anchor=tk.CENTER)

    txt_result = tk.Text(window, height=1, width=80)
    txt_result.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    txt_result.insert(tk.INSERT, data["Resultado"])

    conclusion = tk.Label(window, text="Conclusão")
    conclusion.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

    txt_conclusion = tk.Text(window, height=3, width=80)
    txt_conclusion.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    txt_conclusion.insert(tk.INSERT, data["Conclusão"])

    obs = tk.Label(window, text="Observações")
    obs.place(relx=0.5, rely=0.63, anchor=tk.CENTER)

    txt_obs = tk.Text(window, height=6, width=80)
    txt_obs.place(relx=0.5, rely=0.72, anchor=tk.CENTER)
    txt_obs.insert(tk.INSERT, data["Observações"])

    ass = tk.Label(window, text="Assinatura")
    ass.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    txt_ass = tk.Text(window, height=2, width=80)
    txt_ass.place(relx=0.5, rely=0.85, anchor=tk.CENTER)
    txt_ass.insert(tk.INSERT, data["Assinatura"])

    button_save = tk.Button(window, text="Salvar", command=lambda: save())
    button_save.place(relx=0.2, rely=0.9, anchor=tk.W)

    button_help = tk.Button(window, text="Reset", command=lambda : reset())
    button_help.place(relx=0.4, rely=0.9, anchor=tk.CENTER)

    button_help = tk.Button(window, text="Ajuda", command=lambda : pdf_help())
    button_help.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    button_help = tk.Button(window, text="Default", command=lambda : default())
    button_help.place(relx=0.6, rely=0.9, anchor=tk.CENTER)

    button_preview = tk.Button(window, text="Visualizar", command=lambda: preview())
    button_preview.place(relx=0.8, rely=0.9, anchor=tk.E)


def edit_pdf():
    """
    Allows the user to edit the PDF template used.
    """
    # Get all data
    filename = "pdf_user_template.json" if os.path.isfile(get_file("pdf_user_template.json")) else "pdf_template.json"

    with open(get_file(filename), 'r', encoding='utf8') as fl:
        data = json.load(fl)

    window = tk.Tk()
    window.title("Edit PDF")
    window.geometry('800x800')

    _edit_pdf(window, data)

    window.mainloop()


def email_help():
    window = tk.Tk()
    window.title("Ajuda: Editor de Email")
    window.geometry('700x500')

    text = """
Digite nos campos possíveis as modificações desejadas no template de email.

Aperte o botão reset para descartar as modificações.
Aperte o botão "Salvar" para salvar suas alterações.
Aperte o botão "Reset" para desfazer as alterações.
Aperte o botão "Default" e aperte salvar para utilizar o template padrão.
Aperte o botão "Ver positivo" para poder visualizar o email de resultado positivo conforme os dados inserido.
Aperte o botão "Ver negativo" para poder visualizar o email de resultado negativo conforme os dados inserido.
Aperte o botão "Ver inconclusivo" para poder visualizar o email de resultado inconclusivo conforme os dados inserido.
As alterações feitas não serão salvas caso se feche a janela do editor de email sem apertar o botão "Salvar".

As seguintes variáveis podem ser inseridas no pdf escrevendo-as entre chaves ({ }):

nome do paciente = "{name}"
data de coleta da amostra = "{date}"
    """

    lbl = tk.Label(window, text=text, font=("Arial", 10, "bold"), wraplength=500)
    lbl.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    lbl.pack()

    window.mainloop()


def _edit_email(window, data):

    def save():
        """
        Saves the user changes.
        """
        data["corpo 1"] = txt_c1.get("1.0",'end-1c')
        data["positivo"] = txt_pos.get("1.0",'end-1c')
        data["negativo"] = txt_neg.get("1.0",'end-1c')
        data["inconclusivo"] = txt_inc.get("1.0",'end-1c')
        data["corpo 2"] = txt_c2.get("1.0",'end-1c')
        data["assinatura"] = txt_ass.get("1.0",'end-1c')

        with open(get_file("email_user_template.json"), "w", encoding='utf8') as fl:
            json.dump(data, fl, ensure_ascii=False, indent=0)

        show_info_box("Dados salvos!")

    def preview(resultado):
        """
        Allows the user to preview the changes he made.
        """
        _data = {}
        _data["corpo 1"] = txt_c1.get("1.0",'end-1c')
        _data["positivo"] = txt_pos.get("1.0",'end-1c')
        _data["negativo"] = txt_neg.get("1.0",'end-1c')
        _data["inconclusivo"] = txt_inc.get("1.0",'end-1c')
        _data["corpo 2"] = txt_c2.get("1.0",'end-1c')
        _data["assinatura"] = txt_ass.get("1.0",'end-1c')

        text = _data["corpo 1"] + _data[resultado] + _data["corpo 2"] + _data["assinatura"]

        _window = tk.Tk()
        _window.title("Preview " + resultado)
        _window.geometry('600x500')

        lbl = tk.Label(_window, text=text, wraplength=500)
        lbl.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        _window.mainloop()

    def default():
        with open(get_file("email_template.json"), 'r', encoding='utf8') as fl:
            data = json.load(fl)
        
        _edit_email(window, data)

    def reset():
        filename = "email_user_template.json" if os.path.isfile(get_file("email_user_template.json")) else "email_template.json"

        with open(get_file(filename), 'r', encoding='utf8') as fl:
            data = json.load(fl)
        
        _edit_email(window, data)


    title = tk.Label(window, text="Editor do template de Emails", font=("Arial", 15, "bold"))
    title.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

    c1 = tk.Label(window, text="Corpo 1")
    c1.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    txt_c1 = tk.Text(window, height=3, width=80)
    txt_c1.place(relx=0.5, rely=0.15, anchor=tk.CENTER)
    txt_c1.insert(tk.INSERT, data["corpo 1"])

    pos = tk.Label(window, text="Resultado positivo")
    pos.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    txt_pos = tk.Text(window, height=3, width=80)
    txt_pos.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
    txt_pos.insert(tk.INSERT, data["positivo"])

    neg = tk.Label(window, text="Resultado negativo")
    neg.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    txt_neg = tk.Text(window, height=3, width=80)
    txt_neg.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
    txt_neg.insert(tk.INSERT, data["negativo"])

    inc = tk.Label(window, text="Resultado inconclusivo")
    inc.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    txt_inc = tk.Text(window, height=3, width=80)
    txt_inc.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
    txt_inc.insert(tk.INSERT, data["inconclusivo"])

    c2 = tk.Label(window, text="Corpo 2")
    c2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    txt_c2 = tk.Text(window, height=3, width=80)
    txt_c2.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
    txt_c2.insert(tk.INSERT, data["corpo 2"])

    ass = tk.Label(window, text="Assinatura")
    ass.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    txt_ass = tk.Text(window, height=3, width=80)
    txt_ass.place(relx=0.5, rely=0.65, anchor=tk.CENTER)
    txt_ass.insert(tk.INSERT, data["assinatura"])

    button_save = tk.Button(window, text="Salvar", command=lambda: save())
    button_save.place(relx=0.1, rely=0.9, anchor=tk.W)

    button_help = tk.Button(window, text="Reset", command=lambda : reset())
    button_help.place(relx=0.21, rely=0.9, anchor=tk.CENTER)

    button_help = tk.Button(window, text="Ajuda", command=lambda : email_help())
    button_help.place(relx=0.3, rely=0.9, anchor=tk.CENTER)

    button_help = tk.Button(window, text="Default", command=lambda : default())
    button_help.place(relx=0.39, rely=0.9, anchor=tk.CENTER)

    button_preview = tk.Button(window, text="Ver positivo", command=lambda: preview("positivo"))
    button_preview.place(relx=0.55, rely=0.9, anchor=tk.E)
    
    button_preview = tk.Button(window, text="Ver negativo", command=lambda: preview("negativo"))
    button_preview.place(relx=0.7, rely=0.9, anchor=tk.E)

    button_preview = tk.Button(window, text="Ver inconclusivo", command=lambda: preview("inconclusivo"))
    button_preview.place(relx=0.88, rely=0.9, anchor=tk.E)

def edit_email():
    """
    Allows the user to edit the email body
    """
    filename = "email_user_template.json" if os.path.isfile(get_file("email_user_template.json")) else "email_template.json"

    with open(get_file(filename), 'r', encoding='utf8') as fl:
        data = json.load(fl)

    window = tk.Tk()
    window.title("Edit Email")
    window.geometry('800x800')

    _edit_email(window, data)

    window.mainloop()


def main_window(parse_data):

    def sending_email_text():
        global sending_emails_trigger

        if sending_emails_trigger:
                txt_entry.configure(state = "disabled")
                txt_label.configure(text = "Mandando emails")
                # Update window to disable the txt_entry and change the text of txt_label
                window.update()
                sending_emails_trigger = False
                window.after(100, sending_email_text)
        else: window.after(100, sending_email_text)

    def refresh_text():
        global refresh_trigger

        if refresh_trigger:
            txt_entry.configure(state = "normal")
            txt_entry.delete(0, "end")
            txt_label.configure(text = "Selecione o número dos pacientes cujo laudo deve ser mandado")
            refresh_trigger = False
            window.after(100, refresh_text)
        else: window.after(100, refresh_text)


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

    button_send = tk.Button(window, text="Enviar Emails", command=lambda: parse_data(window, txt_entry, txt_label))
    button_send.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    button_edit_pdf = tk.Button(window, text="Editar template PDF", command=lambda: edit_pdf())
    button_edit_pdf.place(relx=0.3, rely=0.8, anchor=tk.CENTER)

    button = tk.Button(window, text="Editar template Emails", command=lambda: edit_email())
    button.place(relx=0.7, rely=0.8, anchor=tk.CENTER)
    
    window.bind('<Return>', lambda x: parse_data(window, txt_entry, txt_label))

    window.after(100, sending_email_text)
    window.after(100, refresh_text)

    window.mainloop()
