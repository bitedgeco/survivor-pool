# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
)

from .meta import Base


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    week = Column(Integer)
    datetime = Column(DateTime)
    home = Column(Text)
    away = Column(Text)
    winner = Column(Text)
    user_list = relationship("Pick", back_populates="event")
