# fastapi_app


$ alembic init alembic

In alembic.ini:
sqlalchemy.url = <database_url>

In alembic/env.py:
from app.models import Base
target_metadata = Base.metadata

Create tables:
$ alembic revision --autogenerate -m "Create tables"
$ alembic upgrade head


