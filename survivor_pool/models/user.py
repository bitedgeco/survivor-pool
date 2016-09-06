# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
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
    event = relationship("Pick", back_populates="user_list")

    # def __repr__(self):
    #     return "user: {}".format(self.username)

    # color = "blue"
