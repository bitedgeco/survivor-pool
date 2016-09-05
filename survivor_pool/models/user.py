# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    UnicodeText,
    DateTime,
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


# Index('user_index', User.name, unique=True, mysql_length=255)
