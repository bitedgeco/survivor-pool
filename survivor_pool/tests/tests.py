# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..models import (
    User,
    Event,
    Pick,
)
import datetime
from pyramid.httpexceptions import HTTPFound

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
    response = testapp.get('/admin/week9', status='3*')
    assert response.status_code == 302


def test_pool_redirect(testapp):
    '''Test redirect of non-logged in user from pool.'''
    response = testapp.get('/pool', status='3*')
    assert response.status_code == 302


def test_pick_redirect(testapp):
    '''Test redirect of non-logged in user from select.'''
    response = testapp.get('/pick/week9', status='3*')
    assert response.status_code == 302


def test_private_view_accessible(auth_app):
    """Test if authenticated app can access restricted page."""
    response = auth_app.get('/pick/week9', status=200)
    assert b'Seahawks' in response.body


def test_admin_view_inaccessible(auth_app):
    """Test if an authenticated user gets redirected at the admin page."""
    response = auth_app.get('/admin/week9', status='3*')
    assert response.status_code == 302


def test_private_view_accessible_admin(admin_app):
    """Test if admin app can access restricted page."""
    response = admin_app.get('/pick/week9', status=200)
    assert b'Seahawks' in response.body


def test_admin_view_accessible_for_admin(admin_app):
    """Test if an admin has access to the admin pages."""
    response = admin_app.get('/admin/week9', status=200)
    assert b'Seahawks' in response.body


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


def test_admin_view_post_request_keys(dummy_request, populated_db):
    """Test admin view with a post request for dict outcome."""
    from ..views.default import admin_view
    dummy_request.matchdict["week_num"] = 2
    dummy_request.method = "POST"
    result = admin_view(dummy_request)
    expected_result = ["games", "week", "current_week", "teams"]
    assert all(names in result.keys() for names in expected_result)


def test_admin_view_post_request_chk_listofgames(dummy_request, populated_db):
    """Test admin view with a post request for specific content."""
    from ..views.default import admin_view
    dummy_request.matchdict["week_num"] = 2
    dummy_request.method = "POST"
    result = admin_view(dummy_request)
    assert len(result["games"]) == 6


def test_login_view_invalid_credentials(dummy_request):
    """Test login view with invalid login credentials."""
    from ..views.default import login_view
    auth_data = {
        "username": "Bob Marley",
        "password": "groovy man",
    }
    dummy_request.params = auth_data
    dummy_request.method = "POST"
    assert login_view(dummy_request) == {'login_error': 'invalid credentials'}


def test_login_view_new_username_valid_return_val(dummy_request, populated_db):
    """Test login with new username that is valid, ensure return is correct."""
    from ..views.default import login_view
    new_user_data = {
        "new_username": "Bob Marley",
        "new_password": "groovy man",
    }
    dummy_request.params = new_user_data
    dummy_request.method = "POST"
    assert isinstance(login_view(dummy_request), HTTPFound)


def test_login_view_new_username_valid_check_new_user(dummy_request, populated_db):
    """Test login with new username that is valid, ensure new user is in
    dbsession.dirty."""
    from ..views.default import login_view
    new_user_data = {
        "new_username": "Bob Marley",
        "new_password": "groovy man",
    }
    dummy_request.params = new_user_data
    dummy_request.method = "POST"
    login_view(dummy_request)
    new_user = dummy_request.dbsession.new.pop()
    assert isinstance(new_user, User)


def test_login_view_new_username_already_exists(dummy_request, populated_db):
    """Test login new username with username that already exists."""
    from ..views.default import login_view
    new_user_data = {
        "new_username": "Bob Barker",
        "new_password": "groovy man",
    }
    dummy_request.params = new_user_data
    dummy_request.method = "POST"
    assert login_view(dummy_request) == {'signup_error': 'user already exists'}


def test_week_view_with_week_out_of_range(dummy_request, populated_db):
    from ..views.default import week_view
    dummy_request.matchdict["week_num"] = 21
    assert isinstance(week_view(dummy_request), HTTPFound)


def test_week_view_get_request(dummerrequest, populated_db):
    from ..views.default import week_view
    dummerrequest.authenticated_userid = "Bob Barker"
    dummerrequest.matchdict["week_num"] = 3
    dummerrequest.method = "GET"
    expected_result = ["games", "week", "past_picks", "teams", "past_full",
                       "weeks_with_no_byes", "current_week"]
    result = week_view(dummerrequest)
    assert all(names in result.keys() for names in expected_result)


def test_week_view_post_request_output(dummerrequest, populated_db):
    from ..views.default import week_view
    dummerrequest.authenticated_userid = "Bob Barker"
    dummerrequest.matchdict["week_num"] = 5
    dummerrequest.method = "POST"
    dummerrequest.params = {"game": "away 1 1"}
    assert isinstance(week_view(dummerrequest), HTTPFound)


def test_week_view_post_request_creates_new_pick(dummerrequest, populated_db):
    from ..views.default import week_view
    dummerrequest.authenticated_userid = "Bob Barker"
    dummerrequest.matchdict["week_num"] = 5
    dummerrequest.method = "POST"
    dummerrequest.params = {"game": "away 1 1"}
    week_view(dummerrequest)
    new_pick = dummerrequest.dbsession.new.pop()
    assert isinstance(new_pick, Pick)


def test_pool_view_output(dummy_request, populated_db):
    from ..views.default import pool_view
    expected_result = ["users", "week", "events"]
    result = pool_view(dummy_request)
    assert all(names in result.keys() for names in expected_result)
