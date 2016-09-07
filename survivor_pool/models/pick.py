# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    ForeignKey,
)

from .meta import Base


class Pick(Base):
    __tablename__ = 'picks'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'), primary_key=True)
    team = Column(Unicode)
    week = Column(Integer)
    user_list = relationship("User", back_populates="event")
    event = relationship("Event", back_populates="user_list")
