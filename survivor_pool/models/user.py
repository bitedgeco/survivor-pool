# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    Boolean,
)

from .meta import Base
from .pick import Pick


class User(Base):
    """Model for a user."""

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode)
    password = Column(Unicode)
    isadmin = Column(Boolean)
    isalive = Column(Boolean)
    event = relationship("Pick", back_populates="user_list")

    def _add_pick(self, event_picked, team_picked, week):
        """Will add a new pick and connect to the user."""
        new_pick = Pick(team=team_picked)
        new_pick.event = event_picked
        new_pick.week = week
        new_pick.user_list = self
        return new_pick

    def _get_pick_for_week(self, week):
        """Get the name of the team picked in week.
        Returns team name or "user didn't pick" string if user didn't make
        a selection for that week.
        """
        try:
            picked_name_in_list = [getattr(pick.event, pick.team) for pick in
                                   self.event if pick.event.week == week]
            return picked_name_in_list[0]
        except IndexError:
            return "User didn't pick a team for this week."

    def _get_all_user_picks(self):
        """Get the team names of all previous picks the user has made and
        returns the in a list."""
        try:
            list_of_picks = [getattr(pick.event, pick.team) for pick in self.event]
            return list_of_picks
        except IndexError:
            return []
