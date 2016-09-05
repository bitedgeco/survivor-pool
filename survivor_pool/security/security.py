# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Everyone, Authenticated, Allow


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
    config.set_default_permission('public')
    config.set_root_factory(UserAuth)


class UserAuth(object):

    def __init__(self, request):
        self.request = request

    __acl__ = [
        (Allow, Everyone, 'public'),
        (Allow, Authenticated, 'private')
        (Allow, 'admin', 'admin')
    ]
