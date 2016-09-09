from pyramid.response import Response
from pyramid.view import view_config
from ..security import check_credentials
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from ..models.user import User
from ..models.pick import Pick
from ..models.event import Event
from ..scripts.helper import find_current_week
from ..scripts.helper import classable_text_conversion


@view_config(route_name='home', renderer='templates/home.jinja2', permission='public')
def home_view(request):
    current_week = find_current_week(request)
    return {"current_week": current_week}


@view_config(route_name='about', renderer='templates/about.jinja2', permission='public')
def about_view(request):
    return {}


@view_config(route_name='admin', renderer='templates/admin.jinja2', permission='admin')
def admin_view(request):
    from ..models.team import Team
    from ..models.event import Event
    list_of_weeks_with_no_byes = [1, 2, 3, 12, 14, 15, 16, 17]
    list_of_teams = request.dbsession.query(Team).all()
    week = int(request.matchdict.get('week_num', None))
    list_of_games = request.dbsession.query(Event).filter(Event.week == week).all()
    current_week = find_current_week(request)
    if request.method == 'GET':
        return {"games": list_of_games, "week": week, "teams": list_of_teams, "weeks_with_no_byes": list_of_weeks_with_no_byes}
    if request.method == 'POST':
        admin_view_post_helper(request)
        for game in list_of_games:
            game._resolve_week()
        return {"games": list_of_games, "week": week, "current_week": current_week, "teams": list_of_teams, "weeks_with_no_byes": list_of_weeks_with_no_byes}


def admin_view_post_helper(request):
    """Update database when admin results weeks games."""
    for game in request.params:
        if game != 'Save pick':
            user_input = str(request.params[game]).split()
            event_id = user_input[1]
            winner = user_input[0]
            event_object = request.dbsession.query(Event).filter(Event.id == event_id).first()
            event_object.winner = winner


@view_config(route_name='login-signup', renderer='templates/login-signup.jinja2', permission='public')
def login_view(request):
    if request.method == 'POST':
        if request.params.get('username', ''):
            username = request.params.get('username', '')
            password = request.params.get('password', '')
            if check_credentials(request, username, password):
                headers = remember(request, username)
                return HTTPFound(location=request.route_url('pool'), headers=headers)
            return {'login_error': 'invalid credentials'}
        if request.params.get('new_username', ''):
            new_username = request.params.get('new_username', '')
            new_password = request.params.get('new_password', '')
            existing_users = request.dbsession.query(User).all()
            if any(d.username == new_username for d in existing_users):
                return {'signup_error': 'user already exists'}
            new_user = User(username=new_username, password=new_password, isalive=True, isadmin=False)
            request.dbsession.add(new_user)
            headers = remember(request, new_username)
            return HTTPFound(location=request.route_url('pool'), headers=headers)
    return {}


@view_config(route_name='pick', renderer='templates/pick.jinja2')
def week_view(request):
    from ..models.team import Team
    from ..models.event import Event
    import json
    list_of_teams = request.dbsession.query(Team).all()
    week = int(request.matchdict.get('week_num', None))
    list_of_weeks_with_no_byes = [1, 2, 3, 12, 14, 15, 16, 17]
    current_week = find_current_week(request)
    if week < current_week or week > 17:
        return HTTPFound(location=request.route_url('pick', week_num=current_week))
    my_user = request.authenticated_userid
    user_object = request.dbsession.query(User).filter(User.username == my_user).one()
    unformatted_past_picks = user_object._get_all_user_picks()
    past_picks = []
    for pick in unformatted_past_picks:
        past_picks.append(classable_text_conversion(pick))
    list_of_games = request.dbsession.query(Event).filter(Event.week == week).all()
    for game in list_of_games:
        game._away = classable_text_conversion(game.away)
        game._home = classable_text_conversion(game.home)

    if request.method == "GET":
        return {
            "games": list_of_games,
            "week": week,
            "past_picks": json.dumps(past_picks),
            "teams": list_of_teams,
            "past_full": unformatted_past_picks,
            "weeks_with_no_byes": list_of_weeks_with_no_byes}

    if request.method == "POST":
        user_input = str(request.params['game']).split()
        game_object = request.dbsession.query(Event).get(user_input[1])
        week = int(user_input[2])
        existing_pick = request.dbsession.query(Pick).filter(Pick.user_id == user_object.id, Pick.week == week).first()
        if existing_pick:
            request.dbsession.delete(existing_pick)
        new_pick = user_object._add_pick(game_object, user_input[0], week)
        request.dbsession.add(new_pick)
        current_week = find_current_week(request)
        return HTTPFound(request.route_url('pick', week_num=week))


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)


@view_config(route_name='pool', renderer='templates/pool.jinja2')
def pool_view(request):
    query = request.dbsession.query(User)
    users = query.order_by(User.username).all()
    week = find_current_week(request) - 1
    events = request.dbsession.query(Event).filter(Event.week == week)
    for user in users:
        user.teamname = user._get_pick_for_week(week)
    return {'users': users, "week": week, "events": events}
