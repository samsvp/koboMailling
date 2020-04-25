import requests
import json
from mailling_system import send_email_report

auth_token = 'auth-token'

form_uid = "form-uid"

sent_status_field = 'relatorio_enviado'
sent_status_param = '\"sim\"'
result_field = 'identificacao/result'

name_field = 'identificacao/nm'
email_field = 'identificacao/eml'

positive_result = 'positivo'
negative_result ='negativo'
inconclusive_result = 'inconclusivo'

positive_message = """
Segue em anexo o Laudo Técnico de Diagnóstico Molecular para o Vírus SARS-CoV2 de exame realizado na UFRJ no dia 02/04/2020.
Solicitamos que retorne esse e-mail nos atualizando sobre o seu estado de saúde atual e que não hesite em contactar em caso de dúvidas.
Torcemos por uma breve recuperação.

Atenciosamente,
Equipe COVID-19 - UFRJ
"""

negative_message = """
Segue em anexo o Laudo Técnico de Diagnóstico Molecular para o Vírus SARS-CoV2 de exame realizado na UFRJ no dia 02/04/2020.

Atenciosamente,
Equipe COVID-19 - UFRJ
"""

inconclusive_message = """
Segue em anexo o Laudo Técnico de Diagnóstico Molecular para o Vírus SARS-CoV2 de exame realizado na UFRJ no dia 02/04/2020. Devido ao resultado inconclusivo, solicitamos que retorne para coleta de nova amostra, de segunda a quinta-feira, entre 8:30-11:30 da manhã, no bloco N do CCS.

Atenciosamente,
Equipe COVID-19 - UFRJ
"""

headers = {'Authorization': 'Token ' + auth_token, 'Content-Type': 'application/json'}

r = requests.get(f'https://kf.kobotoolbox.org/api/v2/assets/{form_uid}/data/?format=json', headers=headers, timeout=10)
registries = r.json()
print(registries)
for registry in registries.get('results'):
    registry_result = registry.get('identificacao/result')
    if registry_result == positive_result:
        print('------------------------Resultado Positivo--------------------------')
        print(registry)
        send_email_report(registry[email_field], f"Prezado {registry[name_field]}, \n" + positive_message)

    elif registry_result == negative_result:
        print('------------------------Resultado Negativo--------------------------')
        print(registry)
        send_email_report(registry[email_field], f"Prezado {registry[name_field]}, \n" + negative_message)

    elif registry_result == inconclusive_result:
        print('------------------------Resultado Inconclusivo--------------------------')
        print(registry)
        send_email_report(registry[email_field], f"Prezado {registry[name_field]}, \n" + inconclusive_message)
