# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Everyone, Authenticated, Allow

from passlib.apps import custom_app_context as pwd_context


class UserAuth(object):

    def __init__(self, request):
        self.request = request

    __acl__ = [
        (Allow, Everyone, 'public'),
        (Allow, Authenticated, 'private')
        (Allow, 'admin', 'admin')
    ]


def check_credentials(username, password):
    """Checks user submitted username and pw against stored pw to determine
    authentication state."""
    gotten_usernames = dbquery_for_usernames
    is_authenticated = False
    if gotten_usernames:
        if username in gotten_usernames:
            gotten_password = dbquery_for_usernames_pw_hash
            try:
                is_authenticated = pwd_context.verify(password, gotten_password)
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
