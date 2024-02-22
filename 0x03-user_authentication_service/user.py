#!/usr/bin/env python3
""" module with SQLAlchemy model 'user' """
from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """ Class mapping for user model """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    email = Column(VARCHAR(250), nullable=False)
    hashed_password = Column(VARCHAR(250), nullable=False)
    session_id = Column(VARCHAR(250), nullable=True)
    reset_token = Column(VARCHAR(250), nullable=True)
