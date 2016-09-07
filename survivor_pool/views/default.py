from pyramid.response import Response
from pyramid.view import view_config
from ..security import check_credentials
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from ..models.user import User
from ..models.pick import Pick
from ..models.event import Event
from ..scripts.helper import find_current_week


@view_config(route_name='home', renderer='templates/home.jinja2', permission='public')
def home_view(request):
    return {}


@view_config(route_name='about', renderer='templates/about.jinja2', permission='public')
def about_view(request):
    return {}


@view_config(route_name='admin', renderer='templates/admin.jinja2')
def admin_view(request):
    return {}


@view_config(route_name='login-signup', renderer='templates/login-signup.jinja2', permission='public')
def login_view(request):
    if request.method == 'POST':
        if request.params.get('username', ''):
            username = request.params.get('username', '')
            password = request.params.get('password', '')
            if check_credentials(request, username, password):
                headers = remember(request, username)
                return HTTPFound(location=request.route_url('pool'), headers=headers)
            login_error = 'invalid credentials'
            return {'login_error': login_error}
        if request.params.get('new_username', ''):
            new_username = request.params.get('new_username', '')
            new_password = request.params.get('new_password', '')
            existing_users = request.dbsession.query(User).all()
            if any(d.username == new_username for d in existing_users):
                signup_error = 'user already exists'
                return {'signup_error': signup_error}
            new_user = User(username=new_username, password=new_password, isalive=True, isadmin=False)
            request.dbsession.add(new_user)
            headers = remember(request, new_username)
            return HTTPFound(location=request.route_url('pool'), headers=headers)
    return {}


@view_config(route_name='pick', renderer='templates/pick.jinja2')
def week_view(request):
    from ..models.event import Event
    week = request.matchdict.get('week_num', None)
    # week = 1
    list_of_games = request.dbsession.query(Event).filter(Event.week == week)
    if request.method == "GET":
        # week = 1
        # determine current week
        # perform appropriate db query for that week
        # display events to user
        return {"games": list_of_games, "week": week}
    if request.method == "POST":
        my_user = request.authenticated_userid
        # import pdb; pdb.set_trace()
        user_input = str(request.params['game']).split()
        game_object = request.dbsession.query(Event).get(user_input[1])
        user_object = request.dbsession.query(User).filter(User.username == my_user).one()
        week = int(user_input[2])

        existing_pick = request.dbsession.query(Pick).filter(User.username == my_user, Pick.week == week).first()
        if existing_pick:
            # import pdb; pdb.set_trace()
            request.dbsession.delete(existing_pick)
        new_pick = user_object._add_pick(game_object, user_input[0], week)
        request.dbsession.add(new_pick)
        return {"games": list_of_games, "week": week}


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)


@view_config(route_name='pool', renderer='templates/pool.jinja2')
def pool_view(request):
    query = request.dbsession.query(User)
    users = query.order_by(User.username).all()
    week = find_current_week(request)
    events = request.dbsession.query(Event).filter(Event.week == week)
    for user in users:
        user.teamname = user._get_pick_for_week(week)
    return {'users': users, "week": week, "events": events}
