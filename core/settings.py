import os
import subprocess
# import ldap 
import json
# from pathlib import Path
import pymysql

from decouple import config
from unipath import Path
# from django_auth_ldap.config import LDAPSearch, LDAPGroupQuery,GroupOfNamesType,PosixGroupType
 
# from pathlib import Path
import pymysql

pymysql.install_as_MySQLdb()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='S#pS3crEt_1122')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# load production server from .env
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS=['https://inneye.com']

API_KEY = "b6b074fcdfc03dad0695d73423bf0b48"

# Application definition
INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'apps.inneye' 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#Login session management
# SESSION_COOKIE_AGE = 86400 # 24 hour

ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "inneye"  
LOGOUT_REDIRECT_URL = "/authentication.urls" 
TEMPLATE_DIR = os.path.join(CORE_DIR, "apps/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'core.wsgi.application'

try:
    DATABASE_NAME = subprocess.check_output(['cat', '/APS/DATABASE_NAME.txt']).decode().strip()
    DATABASE_PASS = subprocess.check_output(['cat', '/APS/MYSQL_ROOT_PASSWORD_FILE.txt']).decode().strip()
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': DATABASE_NAME,
            'USER': 'root',
            'HOST': 'apc-db',
            'PASSWORD': DATABASE_PASS,
            'PORT': '3306',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
            }
        }
    }
except:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'popcorntv',
        'USER': 'popcorntv',
        'PASSWORD': 'server',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
            }
        }
    }
    pass



# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'apps/static'),
)


#############################################################
#############################################################


#### System Logs ####
LOGGING = {
    'version': 1,
    'loggers':{
        'dashboardLogs':{
            'handlers':['infoLogs','warningLogs','errorLogs','criticalLogs','debugLogs','console'],
            'level':DEBUG
        }
    },

    'handlers':{

        'infoLogs':{
            'level':'INFO',
            'class':'logging.FileHandler',
            'filename':str(BASE_DIR)+'/../logs/info.log',
            'formatter':'simple',
        },

        'warningLogs':{
            'level':'WARNING',
            'class':'logging.FileHandler',
            'filename':str(BASE_DIR)+'/../logs/warning.log',
            'formatter':'simple',
        },

        'errorLogs':{
            'level':'ERROR',
            'class':'logging.FileHandler',
            'filename':str(BASE_DIR)+'/../logs/error.log',
            'formatter':'simple',
        },

        'criticalLogs':{
            'level':'CRITICAL',
            'class':'logging.FileHandler',
            'filename':str(BASE_DIR)+'/../logs/critical.log',
            'formatter':'simple',
        },

        'debugLogs':{
            'level':'DEBUG',
            'class':'logging.FileHandler',
            'filename':str(BASE_DIR)+'/../logs/debug.log',
            'formatter':'simple',
        },

        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        }
    },
    
    'formatters':{
        'simple':{
            'format':'{levelname} {asctime} :  {module} {process:d} {message} from function {funcName} in line no. {lineno}',
            'style':'{',
        }
    }
}


# try:
#     with open("creds.json", "r") as f:
#         ldapData = json.load(f)

#     AUTH_LDAP_SERVER_URI = ldapData['AUTH_LDAP_SERVER_URI']
#     AUTH_LDAP_BIND_DN = ldapData['AUTH_LDAP_BIND_DN']
#     AUTH_LDAP_BIND_PASSWORD = ldapData['AUTH_LDAP_BIND_PASSWORD']
#     AUTH_LDAP_USER_SEARCH = LDAPSearch(ldapData['AUTH_LDAP_USER_SEARCH'],ldap.SCOPE_SUBTREE, '(uid=%(user)s)')
#     AUTH_LDAP_GROUP_SEARCH = LDAPSearch(ldapData['AUTH_LDAP_GROUP_SEARCH'],ldap.SCOPE_SUBTREE, '(objectClass=top)')
#     AUTH_LDAP_GROUP_TYPE = PosixGroupType(name_attr="cn")
#     AUTH_LDAP_MIRROR_GROUPS = ldapData['AUTH_LDAP_MIRROR_GROUPS']

#     AUTH_LDAP_PROFILE_ATTR_MAP = ldapData['AUTH_LDAP_PROFILE_ATTR_MAP']

#     AUTH_LDAP_USER_ATTR_MAP = ldapData['AUTH_LDAP_USER_ATTR_MAP']

#     AUTH_LDAP_USER_FLAGS_BY_GROUP = ldapData['AUTH_LDAP_USER_FLAGS_BY_GROUP']

#     AUTH_LDAP_ALWAYS_UPDATE_USER = ldapData['AUTH_LDAP_ALWAYS_UPDATE_USER']
#     AUTH_LDAP_FIND_GROUP_PERMS = ldapData['AUTH_LDAP_FIND_GROUP_PERMS']
#     AUTH_LDAP_CACHE_TIMEOUT = ldapData['AUTH_LDAP_CACHE_TIMEOUT']

#     AUTHENTICATION_BACKENDS = (
#             'django_auth_ldap.backend.LDAPBackend',
#             'django.contrib.auth.backends.ModelBackend',
#     )

# except Exception as err:
#     print(err)
#     print("Unable to  Link LDAP")
#     AUTHENTICATION_BACKENDS = (
#         'django.contrib.auth.backends.ModelBackend',
#     )


# try:
#     conn = ldap.initialize(AUTH_LDAP_SERVER_URI)
#     conn.protocol_version=ldap.VERSION3
#     conn.simple_bind_s( AUTH_LDAP_BIND_DN, AUTH_LDAP_BIND_PASSWORD)

#     LDAP_STATUS = True
#     LDAP_ERR = 0
# except Exception as err:
#     LDAP_STATUS = False
#     LDAP_ERR = err


