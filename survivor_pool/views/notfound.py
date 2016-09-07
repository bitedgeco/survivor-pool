from pyramid.view import notfound_view_config
from pyramid.view import forbidden_view_config
from pyramid.httpexceptions import HTTPFound


@notfound_view_config(renderer='../templates/404.jinja2')
def notfound_view(request):
    # import pdb; pdb.set_trace()
    request.response.status = 404
    return {}


@forbidden_view_config()
def forbidden_view(request):
    request.response.status = 403
    return HTTPFound(location=request.route_url('login-signup'))
