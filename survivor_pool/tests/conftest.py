# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import transaction
from ..models import (
    User,
    Event,
    Pick,
    get_engine,
    get_session_factory,
    get_tm_session,
)

from .test_event_dict import TEST_EVENT_DICT
from .test_pick_dict import TEST_PICK_DICT
from .test_user_dict import TEST_USER_DICT

import datetime
from pyramid import testing
import pytest
from ..models.meta import Base
import os

from passlib.apps import custom_app_context as pwd_context


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


@pytest.fixture(scope='session')
def auth_env():
    username = 'Bob Barker'
    password = 'password'
    os.environ['AUTH_USERNAME'] = username
    os.environ['AUTH_PASSWORD'] = pwd_context.encrypt(password)
    return username, password


@pytest.fixture(scope='function')
def auth_app(testapp, auth_env):
    username, password = auth_env
    auth_data = {
        'username': username,
        'password': password
    }
    testapp.post('/login-signup', auth_data)
    return testapp


@pytest.fixture(scope='session')
def admin_env():
    username = 'Zach'
    password = 'laptop'
    os.environ['AUTH_USERNAME'] = username
    os.environ['AUTH_PASSWORD'] = pwd_context.encrypt(password)
    return username, password


@pytest.fixture(scope='function')
def admin_app(testapp, admin_env):
    username, password = admin_env
    auth_data = {
        'username': username,
        'password': password
    }
    testapp.post('/login-signup', auth_data)
    return testapp


@pytest.fixture(scope="function")
def new_session(sqlengine, request):
    session_factory = get_session_factory(sqlengine)
    session = get_tm_session(session_factory, transaction.manager)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
    session.dbsession = dbsession

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

        for entry in TEST_USER_DICT:
            temp = User(username=entry["username"],
                        password=entry["password"],
                        isadmin=entry["isadmin"],
                        isalive=entry["isalive"])
            dbsession.add(temp)

        for entry in TEST_EVENT_DICT:
            game = Event(week=entry["week"],
                         home=entry["home"],
                         away=entry["away"],
                         datetime=datetime.datetime.strptime(entry["datetime"], "%A %B %d %Y %H:%M"),
                         winner=entry["winner"])
            dbsession.add(game)

        for entry in TEST_PICK_DICT:
            pick = Pick(user_id=entry["user_id"],
                        event_id=entry["event_id"],
                        team=entry["team"],
                        week=entry["week"])
            dbsession.add(pick)

    def teardown():
        with transaction.manager:
            session.query(Pick).delete()
            session.query(User).delete()
            session.query(Event).delete()
    request.addfinalizer(teardown)
