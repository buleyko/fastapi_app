from pydantic import BaseSettings as BaseConfig

__all__ = ('cfg',)



class Congig(BaseConfig):
    server_host: str = '127.0.0.1'
    server_port: int = 8000

    database_url: str = 'sqlite:///./fastapi_test_db.sqlite3'

    languages: list = ['eu', 'ru']

    jwt_secret: str = '*** change me ***'
    jwt_algorithm: str = 'HS256'
    jwt_expires_s: int = 3600
    
    login_router: str ='/auth/sign-in/'

    items_in_list = 15


cfg = Congig(
    _env_file = '.env',
    _env_file_encoding = 'utf-8'
)