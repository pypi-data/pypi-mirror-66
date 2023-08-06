import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

SQL_ALCHEMY_CONN = os.getenv('SQL_ALCHEMY_CONN')

Base = declarative_base()

engine = None
Session = None


def configure_orm():
    global engine
    global Session
    engine_args = {}
    if 'sqlite' not in SQL_ALCHEMY_CONN:
        # Engine args not supported by sqlite
        engine_args['pool_size'] = 5
        engine_args['pool_recycle'] = 1800

    engine = create_engine(SQL_ALCHEMY_CONN, **engine_args)
    Session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine))


configure_orm()
