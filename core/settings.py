import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- SÉCURITÉ ---
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-8vux^m90h)kf2vb+zn2j_7sfsl#jqmo_a5fb7-%p%fy=3zb*e)')

# Cette ligne passe DEBUG à False si on est sur PythonAnywhere OU Render
DEBUG = not any(env in os.environ for env in ['RENDER', 'PYTHONANYWHERE_DOMAIN'])

ALLOWED_HOSTS = ['abtoure.pythonanywhere.com', '127.0.0.1', 'localhost']
render_external_url = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if render_external_url:
    ALLOWED_HOSTS.append(render_external_url)

# --- APPS ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',
    'theme',
    'business',
]

# --- MIDDLEWARE (Ajout de WhiteNoise pour les fichiers statiques) ---
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

ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# --- BASE DE DONNÉES (Auto-adaptative) ---
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

# --- VALIDATION MOTS DE PASSE ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- INTERNATIONALISATION ---
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Abidjan'
USE_I18N = True
USE_TZ = True

# --- FICHIERS STATIQUES ---
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Permet de servir les fichiers compressés pour plus de rapidité
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = ["127.0.0.1"]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'