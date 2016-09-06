# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    Boolean,
)

from .meta import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode)
    password = Column(Unicode)
    isadmin = Column(Boolean)
    isalive = Column(Boolean)

Index('user_index', User.username, unique=True, mysql_length=255)
