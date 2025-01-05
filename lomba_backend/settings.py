from pathlib import Path
from decouple import config
from datetime import timedelta
import os

from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG')

ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')


# Application definition
INSTALLED_APPS = [
    'unfold',
    "unfold.contrib.import_export",
    'unfold.contrib.simple_history',
    'django_cleanup.apps.CleanupConfig',
    'rest_framework',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'ai',
    'analytics',
    'api',
    'destinations',
    'fauna',
    'flora',
    'guides',
    'health',
    'kuliner',
    
    'import_export',
]


LANGUAGES = [
    ("en", "English"),
    ("id", "Indonesian"),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

LANGUAGE_CODE = "en"

UNFOLD = {
    "SITE_TITLE": "Green Haven Management",
    "SITE_HEADER": "Green Haven Management",
    
    "SITE_URL": "/",
    
    "THEME": None,  
    "SHOW_HISTORY": True,  
    "SHOW_VIEW_ON_SITE": True,
    "LANGUAGES": [
        ("en", "English"),
        ("id", "Indonesian"),
    ],
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Main Navigation"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": _("Users & Authentication"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "person",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
            {
                "title": _("Destinations"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Destinations"),
                        "icon": "tour",
                        "link": reverse_lazy("admin:destinations_destinations_changelist"),
                    },
                    {
                        "title": _("Flora"),
                        "icon": "local_florist",
                        "link": reverse_lazy("admin:flora_flora_changelist"),
                    },
                    {
                        "title": _("Fauna"),
                        "icon": "pets",
                        "link": reverse_lazy("admin:fauna_fauna_changelist"),
                    },
                    {
                        "title": _("Culinary"),
                        "icon": "restaurant_menu",
                        "link": reverse_lazy("admin:kuliner_kuliner_changelist"),
                    },
                    {
                        "title": _("Health"),
                        "icon": "medical_services",
                        "link": reverse_lazy("admin:health_health_changelist"),
                    },
                    {
                        "title": _("Guides"),
                        "icon": "person_pin_circle",
                        "link": reverse_lazy("admin:guides_guides_changelist"),
                    },
                ],
            },
            {
                "title": _("Analytics"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Request Log"),
                        "icon": "analytics",
                        "link": reverse_lazy("admin:analytics_requestlog_changelist"),
                    },
                    {
                        "title": _("Compliance Log"),
                        "icon": "security",
                        "link": reverse_lazy("admin:analytics_compliancelog_changelist"),
                    },
                    {
                        "title": _("Custom Event"),
                        "icon": "event_note",
                        "link": reverse_lazy("admin:analytics_customevent_changelist"),
                    },
                    {
                        "title": _("AI Analytics"),
                        "icon": "insights",
                        "link": reverse_lazy("admin:ai_aianalytics_changelist"),
                    },
                    {
                        "title": _("AI Feedback Analytics"),
                        "icon": "feedback",
                        "link": reverse_lazy("admin:ai_aifeedbackanalytics_changelist"),
                    }
                ],
            },
            {
                "title": _("AI Management"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Chatbot Intents"),
                        "icon": "chat",
                        "link": reverse_lazy("admin:ai_intents_changelist"),
                    },
                    {
                        "title": _("Chat Feedback"),
                        "icon": "rate_review",
                        "link": reverse_lazy("admin:ai_chatfeedback_changelist"),
                    },
                ],
            },
        ],
    },
    "COLORS": { 
        "font": {
            "subtle-light": "107 114 128",
            "subtle-dark": "156 163 175",
            "default-light": "75 85 99",
            "default-dark": "209 213 219",
            "important-light": "17 24 39",
            "important-dark": "243 244 246",
        },
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "fr": "🇫🇷",
                "nl": "🇧🇪",
            },
        },
    },
}


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'analytics.middleware.AnalyticsMiddleware',
    'analytics.middleware.ComplianceLoggingMiddleware',
    'ai.middleware.AIAnalyticsMiddleware',
    'ai.middleware.AIFeedbackAnalyticsMiddleware',
]

ROOT_URLCONF = 'lomba_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'lomba_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='property_db'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default='postgres'),
        'HOST': config('DB_HOST', default='127.0.0.1'),
        'PORT': config('DB_PORT', default='5432'),
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

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR / 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

API_BASE_URL = 'http://127.0.0.1:8000/api'  # Development

REQUEST_TIMEOUT = 5  # seconds

API_GEMINI_KEY = config('API_GEMINI_KEY')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True