# Django settings for RightArm project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

import os.path
PROJECT_ROOT = os.path.abspath( os.path.dirname(os.path.dirname( __file__ )) )

ADMINS = (
    ('girish', 'girish.n.s@mahiti.org'),
    ('amol', 'amol.pachpute@mahiti.org'),
    #('pradeep', 'pradeep.kumar@mahiti.org'),
    ('harish', 'harish.t.m@mahiti.org'),
    #('jayaraj', 'jayraj.s.r@mahiti.org'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_ROOT, "rightarm.db"),                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Kolkata'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = '/home/rightarm/RightArm/static'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
#STATIC_ROOT = os.path.join(PROJECT_ROOT,"static")
STATIC_ROOT = '/home/rightarm/RightArm/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, "static"),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '(yoz3al9o9wt9-asopf!$sjb0cz$3_9@t0_*2nbq4pu!4s$s-c'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'social_auth.middleware.SocialAuthExceptionMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'RightArm.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'RightArm.wsgi.application'

TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, 'templates'),
                 os.path.join(PROJECT_ROOT, 'templates/usermanagement'),

    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'ckeditor',
    'django_extensions',
    'RightArmCms',
    'Member',
    'Problems',
    'Projects',
    'Social',
    'Donation',
    'usermanagement',
    'fullhistory',
    'django_extensions',
    'basemodule',
    #'django_facebook',
    'faq',
    'linked_integration',
    'social_auth',
    'django_openid_auth',
    'django_user_agents',
    'registration',
    'register',
    'django.contrib.comments',
    'forums',
    'anonymous',
    'django.contrib.humanize',
    'contact_importer',
    'django_contact_importer',
)
CKEDITOR_UPLOAD_PATH = os.path.join(PROJECT_ROOT, 'static/uploads')

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'height': 300,
        'width': 600,
    },
}



# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTHENTICATION_BACKENDS = (

    'django.contrib.auth.backends.ModelBackend',
    'auth.GoogleBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',

    # add the social_auth authentication backend. We're not using the default
    # ModelBackend, but if you are, leave it in the list.
    'social_auth.backends.contrib.linkedin.LinkedinBackend',

)

# These settings are used by the social_auth app.
LINKEDIN_CONSUMER_KEY = '75wi0ndyj4yyxu' # linkedin calls this the "API Key"
LINKEDIN_CONSUMER_SECRET = 'wJMYh4gWncpHWg1A' # "Secret Key"
# Scope determines what linkedin permissions your app will request when users
# sign up. Linkedin reccomends requesting three.
LINKEDIN_SCOPE = ['r_basicprofile', 'r_emailaddress', 'r_fullprofile']
# Field selectors determine what data social_auth will get from linkedin
LINKEDIN_EXTRA_FIELD_SELECTORS = [
    'email-address',
    'headline',
    'industry',
    'location',
    'summary',
    'specialties',
    'positions',
    'educations',
    'skills',
    'summary',
]


# extra_data determines what data will be stored in a JSON field in the
# UserSocialAuth table. This should parallel the field selectors.
LINKEDIN_EXTRA_DATA = [('id', 'id'),
                       ('first-name', 'first_name'),
                       ('last-name', 'last_name'),] + [
                           (field, field.replace('-', '_'), True)
                           for field in LINKEDIN_EXTRA_FIELD_SELECTORS
                       ]

# See the social_auth docs for all the configuration options
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/social/'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = SOCIAL_AUTH_NEW_USER_REDIRECT_URL
LOGIN_ERROR_URL = '/error/'
#LOGIN_URL = "/accounts/profile/"
LOGIN_URL = '/social/'

OPENID_SSO_SERVER_URL = 'https://www.google.com/accounts/o8/id'

ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_REDIRECT_URL = '/social/'

# SMTP settings

EMAIL_USE_SSL = True
EMAIL_HOST = 'webmail.rightarm.com'
EMAIL_HOST_USER = 'webmaster@rightarm.com'
EMAIL_HOST_PASSWORD = 'ArmRight2014'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # This vairiable is used by django registration app.
#If not given it tries "xyz@localhost" for localhost so works for localhost but throws exception for production server.
# So importtant for live/development server

EMAIL_PORT = 587
SITE_ID = 1


TEMPLATE_CONTEXT_PROCESSORS = (
                                "django.contrib.auth.context_processors.auth",
                               "django.core.context_processors.request",
                           )

# Facebook Login Setting's:

FACEBOOK_APP_ID = '1623442481214536'
FACEBOOK_SECRET_KEY = '7a74e195c99679419fadc30d581620a5'
FACEBOOK_REDIRECT_URL = 'http://rightarm.com/facebook_login_success'


#--------------------------GMAIL ------------------------------------

KEY = '143006857742-4obhll6q0qjh1mt826o8oo4aft52dacs.apps.googleusercontent.com'
SECRET = 'iYwdfLvVuYlqJQhj35zX5eY0'

#GOOGLE_OAUTH2_CLIENT_ID = '143006857742-4obhll6q0qjh1mt826o8oo4aft52dacs.apps.googleusercontent.com'
#GOOGLE_OAUTH2_CLIENT_SECRET = 'iYwdfLvVuYlqJQhj35zX5eY0'

#--------------for invite friends from gmail -------
GOOGLE_CLIENT_ID = '106397316493-jc6ouihq4v5gj9c38hq6058bv2282vm2.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'OLL7BLU83Ek7qtWPWHLJ7uc7'