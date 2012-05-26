# -*- coding: utf-8 -*-
from sqlalchemy import create_engine                                                  
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from marked import app

engine = create_engine(app.config['DATABASE_URI'],
                       convert_unicode=True, echo=app.debug)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base(name='Base')
Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)