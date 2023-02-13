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
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String)
    reset_token = Column(String)
