from get_kobo_data import get_kobo_data
from create_pdf import create_report, get_report
from mailling_system import create_body, send_email_report


kobo_data = get_kobo_data()[-1]

sample_date = kobo_data["_submission_time"].replace("T", " ")
result = kobo_data["identificacao/result"]

body = create_body(result, sample_date)

pdf_data, pdf_name = get_report(create_report(kobo_data))

send_email_report("samuelsimplicio5@gmail.com", body, pdf_data, pdf_name)