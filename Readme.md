# Kobo Mailing

Repository to send emails based on the csv data files created from Kobo during the COVID-19 pandemic.

To use it you must have an gmail server that allows the usage of less secure apps. If you wish to use another email provider, change the line
```python
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
```

to

```python
with smtplib.SMTP_SSL('smtp.yourmailprovider.com', your_ssl_port) as smtp:
```
at the bottom of the mailling_system.py script.

This e-mail body and attachments are pre-programmed based on the Federal University of Rio de Janeiro Center of Science and Health templates, as this project was made for them.

Besides the email address you need to write your user id and project id. It will be loaded automatically if you create a "tokens.json" file containing both. E.g.

```javascript
{
    "form_uid": "your_form_uid",
    "auth_token": "your_auth_token"
}
```
