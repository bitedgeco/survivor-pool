# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Everyone, Authenticated, Allow
from passlib.apps import custom_app_context as pwd_context
from .models.user import User


class UserAuth(object):
    """Class for authenticated User."""

    def __init__(self, request):
        self.request = request

    def __acl__(self):
        """Create an access control list."""
        this_acl = [
            (Allow, Everyone, 'public'),
            (Allow, Authenticated, 'private'),
        ]
        if self.request.authenticated_userid:
            this_user = self.request.dbsession.query(User).filter(User.username == self.request.authenticated_userid).first()
            if this_user.isadmin:
                this_acl.append((Allow, self.request.authenticated_userid, 'admin'))
        return this_acl


def check_credentials(request, username, password):
    """Check user submitted username and pw against stored pw to determine authentication state."""
    gotten_usernames = request.dbsession.query(User).all()
    is_authenticated = False
    if gotten_usernames:
        if any(d.username == username for d in gotten_usernames):
            db_pw = request.dbsession.query(User).filter(User.username == username).first()
            try:
                is_authenticated = pwd_context.verify(password, db_pw.password)
            except ValueError:
                pass
    return is_authenticated


def includeme(config):
    """Security configureation for survivor_pool."""
    auth_secret = os.environ.get('AUTH_SECRET', 'itsaseekrit')
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512'
    )
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    config.set_default_permission('private')
    config.set_root_factory(UserAuth)
