"""Model for events.  Each event instance is a NFL game."""

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
    """Event class to store nfl game data."""

    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    week = Column(Integer)
    datetime = Column(DateTime)
    home = Column(Text)
    away = Column(Text)
    winner = Column(Text)
    user_list = relationship("Pick", back_populates="event")

    def _resolve_week(self):
        """
        Resolve the weeks won/lost games by modifying the User.isalive.
        The isalive property of a users who picked losing teams set to false.
        """
        for pick in self.user_list:
            if self.winner != pick.team:
                pick.user_list.isalive = False
