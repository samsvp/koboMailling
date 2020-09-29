import json
import datetime
from fpdf import FPDF
from utils import get_file


paciente = ""
data_form = ""
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


def create_report(data, template_data, pdf_name="result.pdf"):
    """
    Creates a report based on the patient data.
    Returns the name of the create pdf.
    """
    global paciente, data_form, ID, resultado, dt

    if not pdf_name.endswith(".pdf"): pdf_name += ".pdf"
    print(data)
    paciente = data["Nome:"]
    data_form = data.get("Data do exame:", "")
    ID = str(data["Número de registro:"])
    resultado = data["Resultado:"].title()
    index = data["Indice:"]

    dt = str(datetime.datetime.now()).split(".")[0].split(" ")[0]

    patient = f"NOME DO PACIENTE: {paciente}\n"
    now = f"DATA DE LIBERAÇÃO: {dt}\t"
    sample_date = f"DATA DA COLETA: {data_form}\t"
    Id = f"IDENTIFICAÇÃO: 20COV{ID}\n\n"
    material = "MATERIAL COLETADO: Sangue"

    data_text = patient + now + sample_date + Id + material

    title_font = f(template_data["Fonte_Título"])
    tf_size = f(template_data["Fonte_Título_tamanho"])
    font = f(template_data["Fonte"])
    f_size = f(template_data["Fonte_tamanho"])
    title = f(template_data["Título"])
    foot = f(template_data["Assinatura"])
    methodology = f(template_data["Metodologia"])
    observations = f(template_data["Observações"])
    
    if resultado == "Positivo":
        result = f(template_data["Resultado Positivo"])
        conclusion = f(template_data["Conclusão Positivo"])
    elif resultado == "Negativo":
        result = f(template_data["Resultado Negativo"])
        conclusion = f(template_data["Conclusão Negativo"])
    else:
        result = f(template_data["Resultado Inconclusivo"])
        conclusion = f(template_data["Conclusão Inconclusivo"])

    class PDF(FPDF):

        def header(self):
            self.image(get_file("Header.png"), 10, 8, 200)
            self.set_font(title_font, 'B', int(tf_size))
            self.cell(0, 60, title, align='C')


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
    pdf.body(50, 100, "METODOLOGIA:", methodology)
    pdf.body(50, 115, "ÍNDICE:", result)
    pdf.body(50, 125, "CONCLUSÃO:", conclusion)
    pdf.body(50, 140, "OBSERVAÇÕES:", observations)

    pdf.image(get_file("Footer.png"), 75)

    pdf.output(pdf_name, 'F')

    return pdf_name
