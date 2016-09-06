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
from .pick import Pick


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

    def _add_pick(self, event_picked, team_picked, request):
        new_pick = Pick(team=team_picked)
        new_pick.event = event_picked
        self.event.append(new_pick)
        request.dbsession.add(new_pick)
