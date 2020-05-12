import json
import datetime
from fpdf import FPDF
from utils import get_file


paciente = ""
data_amostra = ""
ID = ""
resultado = ""
dt = ""

def f(non_f_str: str):
    """
    f string implementation for the json variables
    """

    return eval(f'f"""{non_f_str}"""')


def get_report(name):
    """
    Reads a pdf report and returns its bytes and name
    """
    with open(name, 'rb') as f:
        file_data = f.read()
        file_name = f.name

    return file_data, file_name


def create_report(kobo_data, data, pdf_name="result.pdf"):
    """
    Creates a report based on the patient data.
    Returns the name of the create pdf.
    """
    global paciente, data_amostra, ID, resultado, dt

    if not pdf_name.endswith(".pdf"): pdf_name += ".pdf"

    paciente = kobo_data["identificacao/nm"]
    data_amostra = kobo_data["_submission_time"].replace("T", " ")
    ID = kobo_data["_id"]
    resultado = kobo_data["identificacao/result"].title()
    dt = str(datetime.datetime.now()).split(".")[0]

    patient = f"Nome do Paciente: {paciente}\n"
    now = f"Data: {dt}\n"
    sample_date = f"Data de recebimento da amostra: {data_amostra}\n"
    Id = f"Identificação do paciente: {ID}\n"
    material = "Material Coletado: swab/sangue\n"

    data_text = patient + now + sample_date + Id + material

    title_font = f(data["Fonte_Título"])
    tf_size = f(data["Fonte_Título_tamanho"])
    font = f(data["Fonte"])
    f_size = f(data["Fonte_tamanho"])
    title = f(data["Título"])
    foot = f(data["Assinatura"])
    methodology = f(data["Metodologia"])
    result = f(data["Resultado"])
    conclusion = f(data["Conclusão"])
    observations = f(data["Observações"])

    class PDF(FPDF):

        def header(self):
            self.image(get_file("Header.png"), 10, 8, 200)
            self.set_font(title_font, 'B', int(tf_size))
            self.cell(30, 60, title, align='L')


        def footer(self):
            self.set_y(-20)
            self.set_font(font, '', int(f_size))
            self.multi_cell(0, 5, foot, align="C")


        def body(self, x_offset, y_offset, title, text):
            self.set_y(y_offset)
            self.multi_cell(0, 0, title)
            self.set_x(x_offset)
            self.multi_cell(0, 5, text)


    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 12)


    pdf.body(10, 60, "", data_text)
    pdf.body(50, 100, "Metodologia:", methodology)
    pdf.body(50, 120, "Resultado:", result)
    pdf.body(50, 140, "Conclusão:", conclusion)
    pdf.body(50, 160, "Observações:", observations)

    pdf.image(get_file("Footer.png"), 75)

    pdf.output(pdf_name, 'F')

    return pdf_name
