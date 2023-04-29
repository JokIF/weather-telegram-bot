from envparse import env
from pathlib import Path

WAIT_TIME = 0.1
STOP_TIME = 15
default_available_requests = 4

project_dir = Path(__file__).parent.parent
locales_dir = project_dir.parent / 'locales'
assets_dir = project_dir.parent / 'assets'

BOT_TOKEN = env('BOT_TOKEN')
GISMETEO_TOKEN = env('GISMETEO_TOKEN')
USERS_IMGS = Path(env('VOLUME_USER_IMAGES'))
POSTGRESQL_USER = env('POSTGRESQL_USER')
POSTGRESQL_PASSWORD = env('POSTGRESQL_PASSWORD')
POSTGRESQL_HOST = env('POSTGRESQL_HOST')
POSTGRESQL_PORT = env('POSTGRESQL_PORT')
POSTGRESQL_DB = env('POSTGRESQL_DB')
POSTGRESQL_URL = \
    f'postgresql://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}:{POSTGRESQL_PORT}/{POSTGRESQL_DB}'

REDIS_HOST = env('REDIS_HOST')
REDIS_PASSWORD = env('REDIS_PASSWORD')
REDIS_PORT = env('REDIS_PORT')
REDIS_DB = env('REDIS_DB')
