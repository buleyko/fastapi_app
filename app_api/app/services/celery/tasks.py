from .celery import celery
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from app.config import cfg

# 'chart.png', {'Content-ID': '<myimageid>'}
def attach_file_to_email(message, filename, extra_headers=None):
	with open(filename, 'rb') as f:
		file_attachment = MIMEApplication(f.read())
   
	file_attachment.add_header('Content-Disposition', f'attachment; filename= {filename}')

	if extra_headers is not None:
		for name, value in extra_headers.items():
			file_attachment.add_header(name, value)
	message.attach(file_attachment)



@celery.task
def send_email(email_data):
    email_sender = email_data['sender']
    email_password = ''
    email_receiver = email_data['to']

    # Set the subject and body of the email
    subject = email_data['subject']
    html = email_data['html']

    email_message = MIMEMultipart()
    email_message['From'] = email_sender
    email_message['To'] = email_receiver
    email_message['Subject'] = subject

    email_message.attach(MIMEText(html, "html"))

    if cfg.mail_server == 'localhost' and cfg.mail_port == 1025:
        email_string = email_message.as_string()

        server = smtplib.SMTP(cfg.mail_server, cfg.mail_port)
        server.sendmail(email_sender, email_receiver, email_string)
        server.quit()

    if cfg.mail_use_ssl and cfg.mail_port == 465:
        files = email_data.get('files', [])
        for file in files:
            if isinstance(file, tuple):
                file_name, ext_headers = file
            else:
                file_name, ext_headers = (file, None,)
            attach_file_to_email(email_message, file_name, ext_headers):
        email_string = email_message.as_string()
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(cfg.mail_server, cfg.mail_port, context=context) as server:
            server.login(cfg.mail_username, cfg.mail_password)
            server.sendmail(email_sender, email_receiver, email_string)

    if cfg.mail_use_tls and cfg.mail_port == 587:
        files = email_data.get('files', [])
        for file in files:
            if isinstance(file, tuple):
                file_name, ext_headers = file
            else:
                file_name, ext_headers = (file, None,)
            attach_file_to_email(email_message, file_name, ext_headers):
        email_string = email_message.as_string()
        context = ssl.create_default_context()
        with smtplib.SMTP(cfg.mail_server, cfg.mail_port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(cfg.mail_username, cfg.mail_password)
            server.sendmail(email_sender, email_receiver, email_string)



"""
html = '''
    <html>
        <body>
            <h1>Daily S&P 500 prices report</h1>
            <p>Hello, welcome to your report!</p>
            <img src='cid:myimageid' width="700">
        </body>
    </html>
    '''

email_from = 'sender_email@gmail.com'
password = 'xxx'
email_to = 'receiver_email@gmail.com'

date_str = pd.Timestamp.today().strftime('%Y-%m-%d')

email_message = MIMEMultipart()
email_message['From'] = email_from
email_message['To'] = email_to
email_message['Subject'] = f'Report email - {date_str}'

email_message.attach(MIMEText(html, "html"))

attach_file_to_email(email_message, 'chart.png', {'Content-ID': '<myimageid>'})
attach_file_to_email(email_message, 'excel_report.xlsx')
attach_file_to_email(email_message, 'fpdf_pdf_report.pdf')

email_string = email_message.as_string()

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(email_from, password)
    server.sendmail(email_from, email_to, email_string)
"""


"""
from email.message import EmailMessage
import smtplib, ssl
def sender_email(mail_data):
    # Define email sender and receiver
    email_sender = 'write-email-here'
    email_password = 'write-password-here'
    email_receiver = 'write-email-receiver-here'

    # Set the subject and body of the email
    subject = 'Check out my new video!'
    body = '''
    I've just published a new video on YouTube: https://youtu.be/2cZzP9DLlkg
    '''

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    server = smtplib.SMTP(cfg.mail_server, cfg.mail_port)
    server.sendmail(email_sender, email_receiver, em.as_string())
    server.quit()

    # # Add SSL (layer of security)
    # context = ssl.create_default_context()

    # # Log in and send the email
    # with smtplib.SMTP_SSL(cfg.mail_server, cfg.mail_port, context=context) as smtp:
    #   smtp.login(cfg.mail_username, cfg.mail_password)
    #   smtp.sendmail(email_sender, email_receiver, em.as_string())

"""