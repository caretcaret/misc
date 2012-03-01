from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from didigetin.models import initialize_sql

def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    config = Configurator(settings=settings)
    config.add_route('home', '/')
    config.add_route('css', '/.css')
    config.add_route('secret', '/~')
    config.add_route('user', '/{user}')
    config.add_route('college', '/{user}/{college}')
    config.scan()
    return config.make_wsgi_app()

