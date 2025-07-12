from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-i=i2$aqd-2qtaf15-4&7bzyg#f8k7#^ffvip2i--eml$k3eo9m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.100.19', 'localhost', '127.0.0.1', '10.28.0.1']


# Application definition

INSTALLED_APPS = [
    'djangocms_admin_style',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'cms',
    'menus',
    'sekizai',
    'treebeard',
    'djangocms_text_ckeditor',
    'easy_thumbnails',
    'filer',
    'mptt',
    'djangocms_picture',
    'theater_cms',
]

MIDDLEWARE = [
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
]

ROOT_URLCONF = 'theater_config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # Single template directory
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'cms.context_processors.cms_settings',
                'sekizai.context_processors.sekizai',
                'theater_cms.context_processors.user_interaction_session_data',
                'theater_cms.views.home_with_current_event',
                'theater_cms.context_processors.display_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'theater_config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_TZ = True

USE_L10N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Different directory for collected files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Source directory
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media and static files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CMS settings
CMS_TEMPLATES = [
    # English templates
    ('greeting.html', 'Greeting Template'),
    ('base.html', 'Base Template'),
    ('home.html', 'Home Template'),
    ('about.html', 'About Us Template'),
    ('events.html', 'Events Template'),
    ('event_detail.html', 'Event Detail Template'),
    ('q&a.html', 'Questions and Answers Template'),
    ('sponsors.html', 'Sponsors Template'),
    ('feedback.html', 'Feedback Template'),
    ('feedback_thank_you.html', 'Feedback Thank You Template'),
    ('email_subscribe.html', 'Email Subscribe Template'),
    ('intro.html', 'Intro Page'),
    
    # Russian templates (all with _ru suffix)
    ('greeting_ru.html', 'Greeting Template (Russian)'),
    ('base_ru.html', 'Base Template (Russian)'),
    ('home_ru.html', 'Home Template (Russian)'),
    ('about_ru.html', 'About Us Template (Russian)'),
    ('events_ru.html', 'Events Template (Russian)'),
    ('event_detail_ru.html', 'Event Detail Template (Russian)'),
    ('q&a_ru.html', 'Questions and Answers Template (Russian)'),
    ('sponsors_ru.html', 'Sponsors Template (Russian)'),
    ('feedback_ru.html', 'Feedback Template (Russian)'),
    ('feedback_thank_you_ru.html', 'Feedback Thank You Template (Russian)'),
    ('email_subscribe_ru.html', 'Email Subscribe Template (Russian)'),
]

SITE_ID = 1

CMS_CONFIRM_VERSION4 = True

X_FRAME_OPTIONS = 'SAMEORIGIN'
CMS_PERMISSION = True

# This might be causing the issue if it exists in your settings
CMS_TEMPLATE_INHERITANCE = False

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

THUMBNAIL_HIGH_RESOLUTION = True

CMS_PLACEHOLDER_CONF = {
    'theater_logo': {
        'name': 'Theater Logo',
        'plugins': ['TheaterLogoPlugin'],
        'default_plugins': [],
    },
    'theater_name': {
        'name': 'Theater Name',
        'plugins': ['TextPlugin'],
        'default_plugins': [],
    },
    'sponsors_intro': {
        'name': 'Sponsors Introduction',
        'plugins': ['TextPlugin'],
        'default_plugins': [],
    },
    'sponsors_logos': {
        'name': 'Sponsor Logos',
        'plugins': ['SponsorLogoPlugin'],
        'default_plugins': [],
    },
    'copyright_text': {
        'name': 'Copyright Text',
        'plugins': ['TextPlugin'],
        'default_plugins': [],
    },
} 