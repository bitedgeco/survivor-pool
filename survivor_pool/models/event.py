# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
)

from .meta import Base


class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    week = Column(Integer)
    datetime = Column(DateTime)
    home = Column(Text)
    away = Column(Text)
