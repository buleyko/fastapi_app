# fastapi_app

JWT

$ alembic init alembic

In alembic.ini:
sqlalchemy.url = <database_url>

In alembic/env.py:
from app.models import Base,
target_metadata = Base.metadata

Create tables:
$ alembic revision --autogenerate -m "Create tables",
$ alembic upgrade head

Redis:
$ /usr/local/opt/redis/bin/redis-server /usr/local/etc/redis.conf,
(brew services start redis, brew services stop redis)

Celery:
$ celery -A app.services.celery worker -l INFO

Test Mail Server:
$ python3 -m smtpd -c DebuggingServer -n localhost:1025


