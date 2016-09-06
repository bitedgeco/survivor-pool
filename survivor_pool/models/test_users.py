# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from passlib.apps import custom_app_context as pwd_context
import datetime


TEST_USERS = [
    {
        "username": "Bob Barker",
        "password": pwd_context.encrypt("password"),
        "signup": datetime.datetime(2016, 8, 23, 14, 30, 54, 123456),
        "profile": "This is some sample profile text.",
        "placeholder": 17,
        "isadmin": False,
        "isalive": True
    },
    {
        "username": "Ficticious Guy",
        "password": pwd_context.encrypt("ballcap"),
        "signup": datetime.datetime(2016, 8, 17, 14, 30, 54, 123456),
        "profile": "This Guy was eliminated.  How sad for him.",
        "placeholder": 17,
        "isadmin": False,
        "isalive": False
    },
    {
        "username": "James",
        "password": pwd_context.encrypt("headphones"),
        "signup": datetime.datetime(2016, 7, 22, 14, 30, 54, 123456),
        "profile": "James likes Twix.",
        "placeholder": 34,
        "isadmin": True,
        "isalive": True
    },
    {
        "username": "Zach",
        "password": pwd_context.encrypt("laptop"),
        "signup": datetime.datetime(2016, 6, 21, 14, 30, 54, 123456),
        "profile": "Zach laughed at James liking Twix.",
        "placeholder": 97,
        "isadmin": True,
        "isalive": True
    },
    {
        "username": "Derek",
        "password": pwd_context.encrypt("whiteboard"),
        "signup": datetime.datetime(2016, 5, 20, 14, 30, 54, 123456),
        "profile": "Derek likes Tacos.  And Burritos too.",
        "placeholder": 33,
        "isadmin": True,
        "isalive": True
    },
]
