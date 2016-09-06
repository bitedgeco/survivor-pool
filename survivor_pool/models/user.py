# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    UnicodeText,
    DateTime,
    Boolean,
)

from .meta import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode)
    password = Column(Unicode)
    signup = Column(DateTime)
    profile = Column(UnicodeText)
    placeholder = Column(Integer)
    isadmin = Column(Boolean)
    isalive = Column(Boolean)
    children = relationship("Select", back_populates="event")

Index('user_index', User.username, unique=True, mysql_length=255)
