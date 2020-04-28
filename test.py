from get_kobo_data import get_kobo_data
from create_pdf import create_report, get_report

kobo_data = get_kobo_data()[244]

create_report(kobo_data)
# import mailling_system

# message = """
# Segue em anexo o Laudo Técnico de Diagnóstico Molecular para o Vírus SARS-CoV2 de exame realizado na UFRJ no dia [dia do exame].
# Solicitamos que retorne esse e-mail nos atualizando sobre o seu estado de saúde atual e que não hesite em contactar em caso de dúvidas.
# Torcemos por uma breve recuperação.

# Atenciosamente,
# Equipe COVID-19 - UFRJ
# """

# mailling_system.send_email_report("samuelsimplicio5@gmail.com", message)