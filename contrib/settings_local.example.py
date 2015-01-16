DEMOSAUCE_SCAN = '__PATH__/demosauce/scan'

FILE_UPLOAD_TEMP_DIR="/var/tmp/"

MEDIA_ROOT = '__PATH__/static/'
MEDIA_URL = '/static/'

HAYSTACK_WHOOSH_PATH = '__PATH__/whoosh_index'

ADMIN_MEDIA_PREFIX = '/media/'

TEMPLATE_DIRS = (
    '__PATH__/templates/local',
    '__PATH__/templates/global',
    )

JINJA2_TEMPLATE_DIRS = (
    '__PATH__/templates/jinja/global',
    )

UWSGI_EVENT_SERVER = ("127.0.0.1", 3032)
UWSGI_EVENT_SERVER_HTTP = "http://127.0.0.1/demovibes/ajax/monitor/new/"
UWSGI_ID_SECRET = "__UWSGI_ID_SECRET__"

SONG_WEIGHT = {
    'N' : 20,
    1   : 90,
    1.5 : 70,
    2   : 45,
    2.5 : 30,
    3   : 20,
    3.5 : 10,
    4   : 3,
    4.5 : 2,
    5   : 1}

SONG_WEIGHT_BEST = {
    'N' : 6666,
    1   : 6666,
    1.5 : 6666,
    2   : 6666,
    2.5 : 6666,
    3   : 6666,
    3.5 : 20,
    4   : 10,
    4.5 : 3,
    5   : 1}

DJ_RANDOM_MIN_VOTES = 1

# DB
DATABASES = {
    'default': {
        'ENGINE'    : 'django.db.backends.mysql',
        'NAME'      : 'demovibes',
        'USER'      : 'demovibes',
        'PASSWORD'  : '__PASS__',
        'HOST'      : '127.0.0.1',
        'PORT'      : '',
        'OPTIONS'   : {'init_command': 'SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED'},
        }
    }

SEARCH_LIMIT = 200
MAX_SONG_LENGTH = None
DEMOSAUCE_SCAN = "__PATH__/demosauce/scan"

TIME_ZONE = 'UTC'  # Should always be UTC, otherwise time on site, oneliner, queue is broken!

SECRET_KEY = '__RANDOM_SECRET_KEY__'

SONGS_IN_QUEUE = 20
SONG_LOCK_TIME = { 'days' : 0, 'hours' : 0, 'minutes' : 4 }
SONG_LOCK_TIME_RANDOM = { 'days' : 0, 'hours' : 0, 'minutes' : 10 }
SONG_LOCK_TIME_VOTE = { 'days' : 0, 'hours' : 0, 'minutes' : 15 }

PLAY_JINGLES = True

PAGINATE = 5
FORUM_PAGINATE = 15

FILE_UPLOAD_PERMISSIONS = 0644

SCREEN_UPLOAD_WIDTH = 2000
SCREEN_UPLOAD_HEIGHT = 2000

ADMIN_AUTO_APPROVE_UPLOADS = 1
ADMIN_AUTO_APPROVE_GROUP = 1
ADMIN_AUTO_APPROVE_LABEL = 1
ADMIN_AUTO_APPROVE_ARTIST = 1
ADMIN_AUTO_APPROVE_COMPILATION = 1
ADMIN_AUTO_APPROVE_SCREENSHOT = 1

CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

RADIO_STATUS_VOTED_MIN_VOTES = 1
