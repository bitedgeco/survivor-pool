"""View information for the not-found and forbidden routes."""

from pyramid.view import notfound_view_config
from pyramid.view import forbidden_view_config
from pyramid.httpexceptions import HTTPFound


@notfound_view_config(renderer='../templates/404.jinja2')
def notfound_view(request):
    """Will route people to the 404 not-found page."""
    # import pdb; pdb.set_trace()
    request.response.status = 404
    return {}


@forbidden_view_config()
def forbidden_view(request):
    """Route to the login page if not a user, or the homepage if a current user."""
    request.response.status = 403
    if request.authenticated_userid:
        return HTTPFound(location=request.route_url('home'))
    else:
        return HTTPFound(location=request.route_url('login-signup'))
