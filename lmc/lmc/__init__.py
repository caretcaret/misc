from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid_beaker import session_factory_from_settings
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from lmc.models import initialize_sql, user_exists

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    beakerSessionFactory = session_factory_from_settings(settings)
    authn_policy = AuthTktAuthenticationPolicy('kxqyifksuM3pQE9Z7xhbLyzDlVJ07X5OA8lbVNvw',
                                               callback=user_exists)
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,
                          session_factory=beakerSessionFactory,
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)
    # Not using authz_policy with ACL/RootFactory because it blocks entire views.
    # We use our own method of authorization. ACLAuthorizationPolicy is used here
    # because we use AuthTktAuthenticationPolicy and Pyramid requires authz to go
    # with authn.
    config.add_static_view('design', 'lmc:design')
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('register', '/register')
    config.add_route('logout', '/logout')
    config.add_route('events', '/events')
    config.add_route('events_add', '/events/add')
    config.add_route('events_edit', '/events/{eventid:\d+}/edit')
    config.add_route('events_event', '/events/{eventid:\d+}')
    config.add_route('events_register', '/events/{eventid:\d+}/register')
    config.add_route('events_chaperone', '/events/{eventid:\d+}/chaperone')
    config.add_route('events_chaperone_new', '/events/{eventid:\d+}/chaperone/new')
    config.add_route('events_chaperone_info', '/events/{eventid:\d+}/chaperone/info')
    config.add_route('events_calendar', '/events/calendar')
    config.add_route('events_calendar_month', '/events/calendar/{year:\d+}/{month:\d+}')
    config.add_route('news', '/news')
    config.add_route('news_article', '/news/{articleid:\d+}')
    config.add_route('news_create', '/news/create')
    config.add_route('news_edit', '/news/{articleid:\d+}/edit')
    config.add_route('profile', '/members/me')
    config.add_route('members_member', '/members/{memberid:\d+}')
    config.add_route('members', '/members')
    config.add_route('archives', '/archives')
    config.add_route('archives_upload', '/archives/upload')
    config.add_route('archives_edit', '/archives/{fileid:\d+}/edit')
    config.add_route('archives_file', '/archives/{fileid:\d+}')
    config.add_route('archives_download', '/archives/{fileid:\d+}/download')
    config.add_route('discuss', '/discuss')
    config.add_route('photos', '/photos')
    config.add_route('photos_new', '/photos/new')
    config.add_route('photos_album', '/photos/{albumid:\d+}')
    config.add_route('photos_album_add', '/photos/{albumid:\d+}/add')
    config.add_route('photos_album_edit', '/photos/{albumid:\d+}/edit')
    config.add_route('photos_photo', '/photos/{albumid:\d+}/{photoid:\d+}')
    config.add_route('photos_photo_edit', '/photos/{albumid:\d+}/{photoid:\d+}/edit')
    config.add_route('activity', '/activity')
    config.add_route('messages', '/messages')
    config.add_route('messages_new', '/messages/new')
    config.add_route('messages_message', '/messages/{id:\d+}')
    config.add_route('admin', '/admin')
    config.scan()
    return config.make_wsgi_app()

