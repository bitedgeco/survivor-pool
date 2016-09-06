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


class Select(Base):
    __tablename__ = 'select'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    event_id = Column(Integer, ForeignKey('event.id'), primary_key=True)
    team = Column(Unicode)
    parent = relationship("User", back_populates="event")
    child = relationship("Event", back_populates="users")
