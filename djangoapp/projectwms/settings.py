
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR.parent / 'data' / 'web'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE-ME")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv("DEBUG", "0")))

ALLOWED_HOSTS = [
    h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",")
]


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'wmssistem',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'projectwms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
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

WSGI_APPLICATION = 'projectwms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv("DB_ENGINE", "CHANGE-ME"),
        'NAME': os.getenv("POSTGRES_DB",'CHANGE-ME'),
        'USER': os.getenv("POSTGRES_USER", "CHANGE-ME"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD", "CHANGE-ME"),
        'HOST': os.getenv("POSTGRES_HOST", "CHANGE-ME"),
        'PORT': os.getenv("POSTGRES_PORT", "CHANGE-ME"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = DATA_DIR / 'static'


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

INSTALLED_APPS = [
    "jazzmin",  # precisa vir antes do admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "wmssistem", 
]

# Configurações do Jazzmin
JAZZMIN_SETTINGS = {
    "site_title": "Gestão de Validade",
    "site_header": "Administração do Sistema",
    "site_brand": "WMS system",
    "welcome_sign": "Bem-vindo ao Painel de Controle",
    "copyright": "WMS system © 2025",

    # Logo opcional (adicione em static/img/logo.png)
    # "site_logo": "img/logo.png",

    # Ícones para apps e models (FontAwesome)
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "wmssistem.Supplier": "fas fa-truck",
        "wmssistem.Product": "fas fa-box",
        "wmssistem.Batch": "fas fa-warehouse",
    },

    # Organização do menu lateral
    "order_with_respect_to": ["wmssistem"],

    # Estrutura de menu customizada
    "custom_links": {
        "wmssistem": [
            {
                "name": "Dashboard",
                "url": "/dashboard/",
                "icon": "fas fa-chart-pie",
                "permissions": ["auth.view_user"],
            },
            
        ]
    },

    # Layout
    "show_ui_builder": True,  # permite testar temas e cores direto no admin
}

# Configurações adicionais opcionais
JAZZMIN_UI_TWEAKS = {
    "theme": "default",  # temas bootstrap: cosmo, flatly, darkly, etc.
    "dark_mode_theme": "slate",
    "navbar": "navbar-dark navbar-primary",
    "sidebar": "sidebar-dark-primary",
    "footer_fixed": True,
    "background": "bg-dark",

}
