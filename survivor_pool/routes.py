def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('about', '/about')
    config.add_route('admin', '/admin')
    config.add_route('home', '/')
    config.add_route('login-signup', '/login-signup')
    config.add_route('logout', '/logout')
    config.add_route('pool', '/pool')
    config.add_route('pick', '/pick')
    config.add_route('week', '/week/{week_num}')
    config.add_route('pick_test', '/pick_test')
