from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from ..security import check_credentials
from pyramid.httpexceptions import HTTPFound 
from pyramid.security import remember, forget


@view_config(route_name='home', renderer='templates/main.jinja2', permission='public')
def home_view(request):
    return {}


@view_config(route_name='about', renderer='templates/about.jinja2', permission='public')
def about_view(request):
    return {}


@view_config(route_name='admin', renderer='templates/admin.jinja2')
def admin_view(request):
    return {}


@view_config(route_name='login', renderer='templates/login.jinja2', permission='public')
def login_view(request):
    if request.method == 'POST':
        username = request.params.get('username', '')
        password = request.params.get('password', '')
        if check_credentials(request, username, password):
            headers = remember(request, username)
            return HTTPFound(location=request.route_url('home'), headers=headers)
    return {}


@view_config(route_name='pool', renderer='templates/pool.jinja2')
def pool_view(request):
    return {}


@view_config(route_name='select', renderer='templates/select.jinja2')
def select_view(request):
    if request.method == "GET":
        # use the formfield to submit event.target element
        # once we're got that element, get ahold of the week #
        # perform db query for week #
        # populate template with query results
        return {}
    if request.method == "POST":
        # use formfield to submit event.target element
        # ID the element via data-value tag
        # call _add_pick on the User identified from the header and passing in
        # the correct event and home/away team
        # redirect user to the same view again but reloaded with their pick
        return {}
    else:
        # determine current week
        # perform appropriate db query for that week
        # display events to user
        return {}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_survivor-pool_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
