from pyramid.response import Response
from pyramid.view import view_config
from ..security import check_credentials
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from ..models.user import User


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
            return HTTPFound(location=request.route_url('pool'), headers=headers)
    return {}


@view_config(route_name='signup', renderer='templates/signup.jinja2', permission='public')
def signup_view(request):
    if request.method == 'POST':
        new_username = request.params.get('new_username', '')
        new_password = request.params.get('new_password', '')
        existing_users = request.dbsession.query(User).all()
        if any(d.username == new_username for d in existing_users):
            error = 'user already exists'
            return {'error': error}
        new_user = User(username=new_username, password=new_password, isalive=True, isadmin=False)
        request.dbsession.add(new_user)
        headers = remember(request, new_username)
        return HTTPFound(location=request.route_url('pool'), headers=headers)
    return {}


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)


@view_config(route_name='pool', renderer='templates/pool.jinja2')
def pool_view(request):
    query = request.dbsession.query(User)
    participants = query.order_by(User.username).all()
    return {'participants': participants}


@view_config(route_name='select', renderer='templates/select.jinja2')
def select_view(request):
    return {}
