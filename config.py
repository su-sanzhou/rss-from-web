import os.path

def get_database_config():
    database = {"dbname": "rss_from_web",
                "user": "ubuntu",
                "password": "password",
                "host": "127.0.0.1",
                }
    return database

def get_app_config():
    base_dir = os.path.dirname(__file__)
    app_settings = {
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5xxxJ89E=",
        #the home.html,login.html dir:./templates
        'template_path': os.path.join(base_dir, "templates"),
        #the .css,.js dir:./static
        'static_path': os.path.join(base_dir, "static"),
        "xsrf_cookies": True,
    }

    return app_settings

def get_other_config():
    other_settings = {
        "listen_port": 8000,
        # the same with nginx proxy loation
        "home_uri": "/rss-from-web/",
        #the url prefix when visit the rss
        "absolute_uri_prefix": "http://localhost:8000/rss-from-web/",
        "rss_site_uri": "http://localost:8000/",
        "refresh_interval": 12 * 60 #minutes
    }
    return other_settings
