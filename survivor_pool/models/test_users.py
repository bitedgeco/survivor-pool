# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from passlib.apps import custom_app_context as pwd_context


TEST_USERS = [
    {
        "username": "Bob Barker",
        "password": pwd_context.encrypt("password"),
        "isadmin": False,
        "isalive": True
    },
    {
        "username": "Nick",
        "password": pwd_context.encrypt("password"),
        "isadmin": False,
        "isalive": True
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
