from fpdf import FPDF
import datetime


def get_report(name):
    """
    Reads a pdf report and returns its bytes and name
    """
    with open(name, 'rb') as f:
        file_data = f.read()
        file_name = f.name

    return file_data, file_name


def create_report(kobo_data, name="result.pdf"):
    """
    Creates a report based on the patient data.
    Returns the name of the create pdf.
    """

    if not name.endswith(".pdf"): name += ".pdf"

    _patient = kobo_data["identificacao/nm"]
    _sample_date = kobo_data["_submission_time"].replace("T", " ")
    _Id = kobo_data["_id"]
    _result = kobo_data["identificacao/result"]
    _date = str(datetime.datetime.now()).split(".")[0]

    patient = f"Nome do Paciente: {_patient}\n"
    date = f"Data: {_date}\n"
    sample_date = f"Data de recebimento da amostra: {_sample_date}\n"
    Id = f"Identificação do paciente: {_Id}\n"
    material = "Material Coletado: swab/sangue\n"

    data_text = patient + date + sample_date + Id + material

    methodology = "Exame de diagnóstico molecular pelo Método de detecção de RT-PCR em tempo real, \
    com sondas de detecção para SARS-CoV2 (COVID-19)"

    result = f"{_result}".title()

    conclusion = f"A amostra coletada de [x] SW, do paciente na presente data, mostrou-se, \
    {result} para o ácidonucléico do SARS-CoV2."

    observations = "\n\
    (1) No caso de exame POSITIVO o paciente deverá manter-se afastado das, \
    atividades laborais por período mínimo de 14 dias após início dos sintomas. Recomendamos \
    que retorne no 14° dia para coleta de nova amostra para controle de cura.\n \
    (2) No caso do SARS-CoV2 NÃO estar detectável na amostra, deve-se levar em consideração \
    o tipo de material coletado e o tempo transcorrido entre o período de sintomas observados, \
    e a data da coleta da amostra para realização do exame.\n \
    (3) Amostra com detecção indeterminada para o ácido nucléico do SARS-CoV2 sugerimos a realização \
    de nova coleta/exame."


    class PDF(FPDF):

        def header(self):
            self.image("laudo_sars_cov/Header.png", 10, 8, 200)
            # Arial bold 15
            self.set_font('Arial', 'B', 15)
            self.cell(30, 60, 'Laudo Técnico de Diagnóstico Molecular para o Vírus SARS-CoV2 (COVID-19)', align='L')


        def footer(self):
            self.set_y(-20)
            _foot = "Avenida Carlos Chagas Filho, 375, CCS, Bloco A, sala 121, Cidade Universitária,\n\
            Ilha do Fundão, Rio de Janeiro/RJ - CEP 21941-902\n \
            Telefone: 55+21+3938-6384"
            self.set_font('Times', '', 8)
            self.multi_cell(0,5,_foot,align="C")


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

    pdf.image("laudo_sars_cov/Footer.png", 75)

    pdf.output(name, 'F')

    return name


# import os
# os.system('template.pdf')