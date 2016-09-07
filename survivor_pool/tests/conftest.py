# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import transaction
from ..models import (
    User,
    Event,
    get_engine,
    get_session_factory,
    get_tm_session,
)
from ..models.test_users import TEST_USERS
from ..models.events_dict import EVENTS
import datetime
from pyramid import testing
import pytest
from ..models.meta import Base
import os


TEST_DB_URL = os.environ.get('TEST_DB_URL', '')
TEST_DB_SETTINGS = {'sqlalchemy.url': TEST_DB_URL}

# tests are expecting TEST_DB_URL constant to be set in the testers environment
# in the following format:
# TEST_DB_URL="postgres://<<your_username_here>>@localhost:5432/test_survivor_pool"
# you also need to run "createdb test_survivor_pool at the command line"


@pytest.fixture(scope="session")
def provide_test_url():
    return TEST_DB_URL


def dummy_request(new_session):
    return testing.DummyRequest(dbsession=new_session)


@pytest.fixture(scope="function")
def sqlengine(request):
    config = testing.setUp(settings=TEST_DB_SETTINGS)
    config.include("..models")
    settings = config.get_settings()
    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    def teardown():
        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture(scope="function")
def testapp(sqlengine, provide_test_url):
    '''Setup TestApp.'''
    from survivor_pool import main
    app = main({}, **TEST_DB_SETTINGS)
    from webtest import TestApp
    return TestApp(app)


@pytest.fixture(scope="function")
def new_session(sqlengine, request):
    session_factory = get_session_factory(sqlengine)
    session = get_tm_session(session_factory, transaction.manager)

    def teardown():
        transaction.abort()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope="function")
def populated_db(request, sqlengine):
    session_factory = get_session_factory(sqlengine)
    session = get_tm_session(session_factory, transaction.manager)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        for entry in TEST_USERS:
            temp = User(username=entry["username"],
                        password=entry["password"],
                        isadmin=entry["isadmin"],
                        isalive=entry["isalive"])
            dbsession.add(temp)

        for entry in EVENTS:
            game = Event(week=entry["week"],
                         home=entry["home"],
                         away=entry["away"],
                         datetime=datetime.datetime.strptime(entry["datetime"], "%A %B %d %Y %H:%M"))
            dbsession.add(game)

    def teardown():
        with transaction.manager:
            session.query(User).delete()
            session.query(Event).delete()
    request.addfinalizer(teardown)
