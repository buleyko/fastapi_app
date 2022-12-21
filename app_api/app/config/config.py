from pydantic import (
    RedisDsn,
    NameEmail,
    BaseSettings as BaseConfig,
)
from kombu import Exchange, Queue

__all__ = ('cfg',)



class Congig(BaseConfig):
    server_host: str = '127.0.0.1'
    server_port: int = 8000

    database_url: str = 'sqlite:///./fastapi_test_db.sqlite3'

    languages: list = ['eu', 'ru']
    default_lang = 'en'

    jwt_secret: str = '*** change me ***'
    jwt_algorithm: str = 'HS256'
    jwt_expires_s: int = 3600
    
    login_router: str ='/auth/sign-in/'

    items_in_list: int = 15

    
    MAIL_SERVER: str = 'localhost'
    MAIL_PORT: int = 1025
    MAIL_USE_TLS: bool = False
    MAIL_USE_SSL: bool = False
    MAIL_DEBUG: bool = True
    MAIL_USERNAME: str = ''
    MAIL_PASSWORD: str = ''
    MAIL_DEFAULT_SENDER: NameEmail = 'admin@mail.com'
    # MAIL_MAX_EMAILS = None
    # MAIL_SUPPRESS_SEND = True
    # MAIL_ASCII_ATTACHMENTS = False
    
    
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