# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..models import (
    User,
    Event,
    Pick,
)
import pytest
import datetime

# *----------view/route/page tests for non-logged-in users-----------*


def test_home(testapp):
    '''Test status and content of home route/view/page.'''
    response = testapp.get('/', status=200)
    assert b'All picks must be in before' in response.body


def test_about(testapp):
    '''Test status and content of about route/view/page.'''
    response = testapp.get('/about', status=200)
    assert b'Survivor pool is a free and open ' in response.body


def test_login_signup_layout(testapp):
    '''Test status and content of about route/view/page.'''
    response = testapp.get('/login-signup', status=200)
    assert b'Existing user' in response.body


def test_404(testapp):
    '''Test status and content of visiting an address that does not exist.'''
    response = testapp.get('/gobeldygoog', status=404)
    assert b'Not Found' in response.body


def test_logout_redirect(testapp):
    '''Test redirect from logout.'''
    response = testapp.get('/logout', status='3*')
    assert response.status_code == 302


def test_admin_redirect(testapp):
    '''Test redirect of non-logged in user from admin.'''
    response = testapp.get('/admin/week1', status='3*')
    assert response.status_code == 302


def test_pool_redirect(testapp):
    '''Test redirect of non-logged in user from pool.'''
    response = testapp.get('/pool', status='3*')
    assert response.status_code == 302


def test_pick_redirect(testapp):
    '''Test redirect of non-logged in user from select.'''
    response = testapp.get('/pick/week1', status='3*')
    assert response.status_code == 302


def test_event_resolve_week(testapp, dummy_request, populated_db):
    """Test the _resolve_week method of Event class."""
    test_event = dummy_request.dbsession.query(Event).filter(Event.id == 1).first()
    test_event._resolve_week()
    test_user = dummy_request.dbsession.query(User).filter(User.id == 1).first()
    assert test_user.isalive is False


def test_user_add_pick(testapp, dummy_request, populated_db):
    """Test _add_pick method of User class."""
    test_user = dummy_request.dbsession.query(User).filter(User.id == 1).first()
    test_event = dummy_request.dbsession.query(Event).filter(Event.id == 1).first()
    assert isinstance(test_user._add_pick(test_event, "away", 1), Pick)


def test_user_get_pick_for_week(testapp, dummy_request, populated_db):
    """Test _get_pick_for_week method of User class."""
    test_user = dummy_request.dbsession.query(User).filter(User.id == 1).first()
    assert test_user._get_pick_for_week(1) == "Carolina Panthers"


def test_user_get_pick_for_week_error(testapp, dummy_request, populated_db):
    """Test _get_pick_for_week catches IndexError and returns string when no
    pick has been made."""
    test_user = dummy_request.dbsession.query(User).filter(User.id == 1).first()
    assert test_user._get_pick_for_week(11) == "User didn't pick a team for this week."


def test_helper_find_current_week_fixed_date(testapp, dummy_request, populated_db):
    """Test the scripts/helper.py function find_current_week
    with a fixed input."""
    from ..scripts.helper import find_current_week
    current_time = datetime.datetime.strptime('Sunday September 09 2016 16:25', "%A %B %d %Y %H:%M")
    assert find_current_week(dummy_request, current_time) == 4


def test_helper_find_current_week_no_input(testapp, dummy_request, populated_db):
    """Test the scripts/helper.py function find_current_week with test data.

    This test will naturally break in a few months and return None when the
    season dates have all gone by."""
    from ..scripts.helper import find_current_week
    assert int(find_current_week(dummy_request))


def test_helper_find_current_week_no_season_data(testapp, dummy_request):
    """Test the scripts/helper.py function find_current_week with no db data.

    This simulates being out of season and the function returning None."""
    from ..scripts.helper import find_current_week
    assert find_current_week(dummy_request) is None


def test_security_check_credentials_pass(testapp, dummy_request, populated_db):
    """Test security.py check_credentials function works properly."""
    from ..security import check_credentials
    assert check_credentials(dummy_request, "Bob Barker", "password") is True


def test_security_check_credentials_fail(testapp, dummy_request, populated_db):
    """Test security.py check_credentials function returns False for
    an unauthorized user."""
    from ..security import check_credentials
    assert check_credentials(dummy_request, "Cris Ewing", "ice_cream") is False


def test_security_check_credentials_error(testapp, dummy_request, populated_db):
    """Test security.py check_credentials function except try:except block
    passes a ValueError."""
    from ..security import check_credentials
    assert check_credentials(dummy_request, "Bob Barker", "") is False


# -----Security tests--------

def test_private_view_accessible(auth_app):
    """Test if authenticated app can access restricted page."""
    response = auth_app.get('/pick/week1', status=200)
    assert b'Seahawks' in response.body


def test_admin_view_inaccessible(auth_app):
    """Test if an authenticated user gets redirected at the admin page."""
    response = auth_app.get('/admin/week1', status='3*')
    assert response.status_code == 302

def test_private_view_accessible_admin(admin_app):
    """Test if admin app can access restricted page."""
    response = admin_app.get('/pick/week1', status=200)
    assert b'Seahawks' in response.body


def test_admin_view_accessible_for_admin(admin_app):
    """Test if an admin has access to the admin pages."""
    response = admin_app.get('/admin/week1', status=200)
    assert b'Seahawks' in response.body


# --------------


def test_admin_view_post_helper_function_length(dummy_request, populated_db):
    """Test to see if there is one object in dbsession.dirty"""
    from ..views.default import admin_view_post_helper
    dummy_request.params['game1'] = 'home 1 1'
    dummy_request.params['Save pick'] = ''
    admin_view_post_helper(dummy_request)
    assert len(dummy_request.dbsession.dirty) == 1


def test_admin_view_post_helper_function_content(dummy_request, populated_db):
    """Check to see if object in dbsession.dirty has updated value."""
    from ..views.default import admin_view_post_helper
    dummy_request.params['game1'] = 'home 1 1'
    dummy_request.params['Save pick'] = ''
    admin_view_post_helper(dummy_request)
    our_updated_thing = dummy_request.dbsession.dirty.pop()
    assert our_updated_thing.winner == 'home'
