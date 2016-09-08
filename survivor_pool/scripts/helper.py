# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from ..models.event import Event

"""This file contains helper functions that can be called by our site."""


def find_current_week(request, current_time=None):
    """This function returns the current week in the pool for which
    selections can still be made.

    Option: current_time can be keyworded for testing or demonstration
    purposes."""
    current_week = 0
    if current_time is None:
        current_time = datetime.datetime.now()
    all_events = request.dbsession.query(Event).order_by(Event.datetime).all()
    for event in all_events:
        this_week = event.week
        this_datetime = event.datetime
        if this_week != current_week:
            current_week = this_week
            if this_datetime > current_time:
                break
    else:
        current_week = None
    return current_week


def classable_text_conversion(team_name):
    """This function formats strings that are team names so they can be used
    in jinja templates as class names and matched against reliably."""
    new_team_name = team_name.lower().replace(" ", "_")
    return new_team_name
