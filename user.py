#!/usr/bin/env python3
"""
SQLAlchemy Model setup (User), for users database table
using mapping declaration of SQLAlchemy
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    """
    Model for database table named users
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)

    hashed_password = Column(String, nullable=False)
    session_id = Column(String)
    reset_token = Column(String)
