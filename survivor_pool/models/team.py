# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sqlalchemy import (
    Column,
    Integer,
    Text,
)

from .meta import Base


class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    bye_week = Column(Integer)
    icon = Column(Text)
