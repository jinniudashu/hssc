import os
from pathlib import Path
from .router import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialise environment variables
import environ
env = environ.Env()
env_file_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_file_path):
    environ.Env.read_env(env_file_path)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Application definition
INSTALLED_APPS = [
    'registration',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    # our apps
    'analytics',
    'core',
    'dictionaries',
    'icpc',
    'service',

    'hssc.apps.UniversalManagerApp',
    'rest_framework',
    'django_celery_results',
    'django_celery_beat',
    'import_export',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# AUTH_USER_MODEL = 'core.User'

ROOT_URLCONF = 'hssc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hssc.wsgi.application'
ASGI_APPLICATION = 'hssc.asgi.application'

# 设定项目名称，测试数据，子域名，域名
DOMAIN = 'tpacn.com'
PROJECT_NAME = 'Clinic'
PROJECT_TEST_DATA = 'core/management/commands/test_data_clinic.json'
SUBDOMAIN = 'clinic'
DB_HOST = 'db'

# PROJECT_NAME = 'Dental'
# PROJECT_TEST_DATA = 'core/management/commands/test_data_dental.json'
# SUBDOMAIN = 'dental'
# DB_HOST = 'dental_db'

DJANGO_ENV = os.environ.get('DJANGO_ENV', 'prod')
if DJANGO_ENV == 'dev':
    DEBUG = True
    ALLOWED_HOSTS = []
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        },
    }
    REDIS_HOST = 'redis://localhost:6379'
    # REDIS_HOST = 'redis://dental_redis:6379'
else:
    DEBUG = True
    ALLOWED_HOSTS = ["127.0.0.1", f'{SUBDOMAIN}.{DOMAIN}', SUBDOMAIN]
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': DB_HOST,
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASS'),
        }
    }
    REDIS_HOST = 'redis://redis:6379'

DATABASE_ROUTERS = ['hssc.router.DatabaseRouter']

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_HOST],
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'
USE_TZ = True
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# 上传文件路径
MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads/')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# django-registration-redux
ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window; you may, of course, use a different value.
REGISTRATION_AUTO_LOGIN = True # Automatically log the user in.
LOGIN_REDIRECT_URL = '/core/index_customer/' # The page you want users to arrive at after they successful log in
LOGIN_URL = 'accounts/login/' # The page users are directed to if they are not logged in,
SIMPLE_BACKEND_REDIRECT_URL = '/'

# APPEND_SLASH=False

# CELERY SETTINGS
CELERY_BROKER_URL = REDIS_HOST
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_RESULT_BACKEND = 'django-db'
# CELERY BEAT SETTINGS
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
# CELERY 的启动工作数量设置
# CELERY_WORKER_CONCURRENCY = 2
# 每个worker执行了多少任务就会死掉，默认是无限
# CELERY_WORKER_MAX_TASKS_PER_CHILD = 200