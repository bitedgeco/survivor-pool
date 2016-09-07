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

    def _resolve_week(self):
        """Resolves the weeks won/lost games by modifying the isalive
        property of Users who picked losing teams."""
        for pick in self.user_list:
            if self.winner != pick.team:
                pick.user_list.isalive = False
