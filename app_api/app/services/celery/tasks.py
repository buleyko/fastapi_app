from app.config import cfg
from .celery import celery



@celery.task
def send_email(email_msg):
	return f'{email_msg}: 99999999'