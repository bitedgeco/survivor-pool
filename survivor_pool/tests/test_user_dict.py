# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from passlib.apps import custom_app_context as pwd_context


TEST_USER_DICT = [
    {
        "username": "Bob Barker",
        "password": pwd_context.encrypt("password"),
        "isadmin": False,
        "isalive": True
    },
    {
        "username": "Ficticious Guy",
        "password": pwd_context.encrypt("ballcap"),
        "isadmin": False,
        "isalive": False
    },
    {
        "username": "James",
        "password": pwd_context.encrypt("headphones"),
        "isadmin": True,
        "isalive": True
    },
    {
        "username": "Zach",
        "password": pwd_context.encrypt("laptop"),
        "isadmin": True,
        "isalive": True
    },
    {
        "username": "Derek",
        "password": pwd_context.encrypt("whiteboard"),
        "isadmin": True,
        "isalive": True
    },
]
