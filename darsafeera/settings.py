import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-key-change-in-production')

# In production (VERCEL=1) DEBUG must be False
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Allow all hosts for Vercel deployment
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'https://darsafeera-taupe.vercel.app',
    'http://*.vercel.app',
]

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'catalog',
    'whitenoise.runserver_nostatic',
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

ROOT_URLCONF = 'darsafeera.urls'

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
                'catalog.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'darsafeera.wsgi.application'

# ── Database ──────────────────────────────────────────────────────────────────
# Uses SQLite locally; switches to Neon Postgres when DATABASE_URL is set
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    # Strip channel_binding param if present
    DATABASE_URL = DATABASE_URL.replace('&channel_binding=require', '').replace('?channel_binding=require&', '?').replace('?channel_binding=require', '')
    DATABASES['default'] = dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    )
    # Force use of psycopg3 (psycopg)
    if 'ENGINE' in DATABASES['default'] and 'postgresql' in DATABASES['default']['ENGINE']:
        DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_TZ = True

# ── Static Files (WhiteNoise serves them on Vercel) ───────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# ── Media Files (Cloudinary in production) ────────────────────────────────────
CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')
if CLOUDINARY_URL:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    CLOUDINARY_STORAGE = {
        'PREFIX': 'darsafeera'
    }
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Brand Settings ────────────────────────────────────────────────────────────
WHATSAPP_NUMBER = os.getenv('WHATSAPP_NUMBER', '2347068886422')
INSTAGRAM_HANDLE = os.getenv('INSTAGRAM_HANDLE', 'safeeraabba')
CONTACT_EMAIL = os.getenv('CONTACT_EMAIL', 'contact.safeeraabba@gmail.com')

# ── Jazzmin Admin Theme ───────────────────────────────────────────────────────
JAZZMIN_SETTINGS = {
    "site_title": "Dar Safeera Admin",
    "site_header": "Dar Safeera",
    "site_brand": "Dar Safeera",
    "site_logo": "images/placeholders/logo.png",
    "login_logo": "images/placeholders/logo.png",
    "site_icon": "images/placeholders/logo.png",
    "welcome_sign": "Welcome to the Dar Safeera Admin",
    "copyright": "Dar Safeera Luxury Abayas",
    "search_model": ["catalog.Product"],
    "topmenu_links": [
        {"name": "View Site", "url": "/", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "catalog.product": "fas fa-tshirt",
        "catalog.category": "fas fa-tags",
        "catalog.productimage": "fas fa-images",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "custom_css": "css/custom_admin.css",
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-warning",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-warning",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}
