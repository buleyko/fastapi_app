from pathlib import Path
from app.config import cfg
from datetime import datetime



def write_to_log(username: str, log_message=''):
	log_file_path = cfg.log_path
	log_file = log_file_path / 'log.txt'
	with open(log_file, mode='w') as log_file:
		content = f'{username}: {log_message}: {datetime.now()}'
		log_file.write(content)