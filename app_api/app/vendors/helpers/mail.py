import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from email.mime.application import MIMEApplication
from app.config import cfg



def get_mail_text(text_key, **kwargs):
	text = '''\
		Hi,
		How are you?
		Real Python has many great tutorials:
		www.realpython.com'''
	html = '''\
		<html>
	  		<body>
	    		<p>Hi,<br>
	       		How are you?<br>
	       		<a href="http://www.realpython.com">Real Python</a> 
	       		has many great tutorials.
	    		</p>
	  		</body>
		</html>
	'''
	return txt, html



def get_email_body(mail_template):
	pass


def attach_file_to_email(email_message, filename, extra_headers=None):
	with open(filename, 'rb') as f:
		file_attachment = MIMEApplication(f.read())
   
	file_attachment.add_header('Content-Disposition', f'attachment; filename= {filename}')

	if extra_headers is not None:
		for name, value in extra_headers.items():
			file_attachment.add_header(name, value)
	email_message.attach(file_attachment)



def email_sender(receiver_email):
	context = ssl.create_default_context()

	if cfg.mail_use_ssl and cfg.mail_port == 465:
		with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
			server.login(sender_email, password)
			server.sendmail(sender_email, receiver_email, message)


	if cfg.mail_use_tls and cfg.mail_port == 587:
		with smtplib.SMTP(smtp_server, port) as server:
			server.ehlo()
			server.starttls(context=context)
			server.ehlo()
			server.login(sender_email, password)
			server.sendmail(sender_email, receiver_email, message)