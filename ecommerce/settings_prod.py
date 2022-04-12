
from .settings import *
import dj_database_url

#override
DEBUG = False

ALLOWED_HOSTS = ['ecommmerce-app01.herokuapp.com']

#postgres database for production
db_from_env = dj_database_url.config()
DATABASES['default'].update()