from collections import namedtuple
from app.vendors.base.database import Session
from sqlalchemy import select

DB = namedtuple('DB' , 'session select')



def get_db():
    db = DB(Session(), select)
    try:
        yield db
    finally:
        db.session.close()