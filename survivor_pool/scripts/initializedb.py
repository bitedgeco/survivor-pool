import os
import sys
import transaction
import datetime
from pyramid.paster import (
    get_appsettings,
    setup_logging,
)
from pyramid.scripts.common import parse_vars
from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
)
from ..models.user import User
from ..models.test_users import TEST_USERS
from ..models.event import Event
from ..models.events_dict import EVENTS
from ..models.pick import Pick
from ..models.pick_dict import TEST_PICKS
from ..models.team import Team
from ..models.teams_dict import TEAMS


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    settings['sqlalchemy.url'] = os.environ.get('DATABASE_URL', '')

    engine = get_engine(settings)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        for entry in TEST_USERS:
            temp = User(username=entry["username"],
                        password=entry["password"],
                        isadmin=entry["isadmin"],
                        isalive=entry["isalive"])
            dbsession.add(temp)

        for entry in EVENTS:
            game = Event(week=entry["week"],
                         home=entry["home"],
                         away=entry["away"],
                         datetime=datetime.datetime.strptime(entry["datetime"], "%A %B %d %Y %H:%M"))
            dbsession.add(game)

        for entry in TEST_PICKS:
            pick = Pick(user_id=entry["user_id"],
                        event_id=entry["event_id"],
                        team=entry["team"],
                        week=entry["week"])
            dbsession.add(pick)

        for entry in TEAMS:
            team = Team(name=entry["name"],
                        bye_week=entry["bye_week"],
                        icon=entry["icon"])
            dbsession.add(team)
