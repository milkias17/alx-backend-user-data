#!/usr/bin/env python3
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

"""
User database model
"""

Base = declarative_base()


class User(Base):
    """User database model"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))
