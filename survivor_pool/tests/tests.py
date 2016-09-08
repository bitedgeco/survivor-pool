# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
