import os
import sys
import transaction

import datetime
from passlib.apps import custom_app_context as pwd_context

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
)

from ..models.user import User


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


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    settings['sqlalchemy.url'] = os.environ.get('DATABASE_URL', '')

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        for entry in TEST_USERS:
            temp = User(username=entry["username"],
                        password=entry["password"],
                        signup=entry["signup"],
                        profile=entry["profile"],
                        placeholder=entry["placeholder"],
                        isadmin=entry["isadmin"],
                        isalive=entry["isalive"])
            dbsession.add(temp)
