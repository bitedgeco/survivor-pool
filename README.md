# Survivor Pool

![GitHub Logo](https://github.com/bitedgeco/survivor-pool/blob/master/survivor_pool/static/img/logo.png)

###Introduction 
Survivor pool is an app to participate in a season of an NFL survivor pool.

###Rules of a survivor pool

* Every week participants select a team to win a single NFL game.
* Participants are eliminated if their selected team losses.
* Survivors cannot select the team twice.
* The winner(s) of the pool is the person/people who survives the longest.

###Website
http://survivorpool.herokuapp.com/


###Functionality

* Users are able to Log in / Log out of the app.
* Once logged in the Pool page displays who is still alive in the pool and who has been eliminated.
* Picks page displays a weeks worth of football games. Participants have ability to selecet a team for the week.
* Once a particular team has been selected that team cannot be used in following weeks.
* Admin has ability to result games on the admin page.


###Dependancies

* PIP
* Pyramid
Then run $ PIP install -e .


###Coverage
Overall coverage 94%.

```
survivor_pool/tests/tests.py ...................................

---------- coverage: platform darwin, python 2.7.12-final-0 ----------
Name                                          Stmts   Miss  Cover   Missing
---------------------------------------------------------------------------
survivor_pool/__init__.py                        11      0   100%
survivor_pool/models/__init__.py                 25      0   100%
survivor_pool/models/event.py                    17      0   100%
survivor_pool/models/events_dict.py               2      0   100%
survivor_pool/models/meta.py                      6      0   100%
survivor_pool/models/pick.py                     12      0   100%
survivor_pool/models/pick_dict.py                 2      0   100%
survivor_pool/models/team.py                      9      0   100%
survivor_pool/models/teams_dict.py                2      0   100%
survivor_pool/models/test_users.py                3      0   100%
survivor_pool/models/user.py                     31      2    94%   49-50
survivor_pool/routes.py                          10      0   100%
survivor_pool/scripts/__init__.py                 0      0   100%
survivor_pool/scripts/helper.py                  20      0   100%
survivor_pool/scripts/initializedb.py            46     28    39%   27-30, 34-76
survivor_pool/security.py                        36      2    94%   37-38
survivor_pool/tests/__init__.py                   0      0   100%
survivor_pool/tests/conftest.py                  96      0   100%
survivor_pool/tests/test_event_dict.py            2      0   100%
survivor_pool/tests/test_pick_dict.py             2      0   100%
survivor_pool/tests/test_user_dict.py             3      0   100%
survivor_pool/tests/tests.py                    160      0   100%
survivor_pool/views/__init__.py                   0      0   100%
survivor_pool/views/default.py                  101      2    98%   122-123
survivor_pool/views/notfound.py                  11      0   100%
---------------------------------------------------------------------------
TOTAL                                           607     34    94%
```
```
survivor_pool/tests/tests.py ...................................

---------- coverage: platform darwin, python 3.5.2-final-0 -----------
Name                                          Stmts   Miss  Cover   Missing
---------------------------------------------------------------------------
survivor_pool/__init__.py                        11      0   100%
survivor_pool/models/__init__.py                 25      0   100%
survivor_pool/models/event.py                    17      0   100%
survivor_pool/models/events_dict.py               2      0   100%
survivor_pool/models/meta.py                      6      0   100%
survivor_pool/models/pick.py                     12      0   100%
survivor_pool/models/pick_dict.py                 2      0   100%
survivor_pool/models/team.py                      9      0   100%
survivor_pool/models/teams_dict.py                2      0   100%
survivor_pool/models/test_users.py                3      0   100%
survivor_pool/models/user.py                     31      2    94%   49-50
survivor_pool/routes.py                          10      0   100%
survivor_pool/scripts/__init__.py                 0      0   100%
survivor_pool/scripts/helper.py                  20      0   100%
survivor_pool/scripts/initializedb.py            46     28    39%   27-30, 34-76
survivor_pool/security.py                        36      2    94%   37-38
survivor_pool/tests/__init__.py                   0      0   100%
survivor_pool/tests/conftest.py                  96      0   100%
survivor_pool/tests/test_event_dict.py            2      0   100%
survivor_pool/tests/test_pick_dict.py             2      0   100%
survivor_pool/tests/test_user_dict.py             3      0   100%
survivor_pool/tests/tests.py                    160      0   100%
survivor_pool/views/__init__.py                   0      0   100%
survivor_pool/views/default.py                  101      2    98%   122-123
survivor_pool/views/notfound.py                  11      0   100%
---------------------------------------------------------------------------
TOTAL                                           607     34    94%
```

###License
MIT License


### Authors

__James Canning__ 

* Website: [Bitedge](https://www.bitedge.co/)

* Git Hub:[github.com/bitedgeco](https://github.com/bitedgeco)


__Derek Hewitt__

* Email: <derekmhewitt@gmail.com>

* Git Hub: [github.com/derekmhewitt](https://github.com/derekmhewitt)


__Zach Rickert__

* Email: <zachrickert@gmail.com>

* Git Hub: [github.com/zachrickert](https://github.com/zachrickert)


### Cited Sources

We received significant help from our instructors, big thanks to Cris Ewing, Nicholas Hunt-Walker and Will Weatherford.

Also got some testing help with testing from the deal-thief team (see dummerrequest in our conftest).
https://github.com/deal-thief/deal-thief
