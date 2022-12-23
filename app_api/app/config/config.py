from pydantic import (
    RedisDsn,
    EmailStr,
    DirectoryPath,
    BaseSettings as BaseConfig,
)
from kombu import Exchange, Queue

__all__ = ('cfg',)



class Congig(BaseConfig):
    server_host: str = '127.0.0.1'
    server_port: int = 8000
    secret_key: str = '*** change me ***'
    root_path: DirectoryPath = '/Users/qrs/Projects/http/fastapi_app/app_api/app'
    resources_dir: str = 'resources'

    database_url: str = 'sqlite:///./fastapi_test_db.sqlite3'

    languages: list = ['eu', 'ru']
    default_lang = 'en'

    jwt_secret: str = '*** change me ***'
    jwt_algorithm: str = 'HS256'
    jwt_expires_s: int = 3600
    
    login_router: str ='/auth/sign-in/'

    items_in_list: int = 15

    
    mail_server: str = 'localhost'
    mail_port: int = 1025
    mail_use_tls: bool = False
    mail_use_ssl: bool = False
    mail_username: str = ''
    mail_password: str = ''
    mail_default_sender: EmailStr = 'admin@mail.com'
    mail_max_emails: int | None = None
    
    
    broker: RedisDsn = 'redis://0.0.0.0:6379/0'
    result_backend: RedisDsn = 'redis://0.0.0.0:6379/0'
    task_serializer: str = 'json'
    accept_content: list = ['json',]

    task_queues: tuple = (
        Queue('high', Exchange('high'), routing_key='high'),
        Queue('normal', Exchange('normal'), routing_key='normal'),
        Queue('low', Exchange('low'), routing_key='low'),
    )
    task_default_queue: str = 'normal'
    task_default_exchange: str = 'normal'
    task_default_routing_key: str = 'normal'
    task_routes: dict = {
        # -- HIGH PRIORITY QUEUE -- #
        # -- NORMAL PRIORITY QUEUE -- # 
        'app.tasks.mail.send_async_email': {'queue': 'normal'},
        # -- LOW PRIORITY QUEUE -- #
    }
    


cfg = Congig(
    _env_file = '.env',
    _env_file_encoding = 'utf-8'
)