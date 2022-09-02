# -*- coding: utf-8 -*-
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-i9k)yrn5=efxuq92$9m92n=t22q16p$r^!$5ffc)92r%8aj@eg'

DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 跨域
    'corsheaders',
    # apps
    'xia.apps.ModelsConfig',
    # 本地代理Swagger文档
    'ninja'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    # 请求记录中间件
    'xia.middleware.access_middleware.AccessMiddleware',
]

ROOT_URLCONF = 'ninja_xia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'ninja_xia.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ninja_xia',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}

# Redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 5,  # seconds
            "SOCKET_TIMEOUT": 5,  # seconds
            "CONNECTION_POOL_KWARGS": {"max_connections": 100, 'decode_responses': True},
        }
    }
}

# Password validation
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
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# static
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

# media path
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'static/media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 跨域
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'DELETE',
    'PATCH',
)

# NinjaAPI
NINJA_TITLE = 'NinjaXia自动化测试平台'
NINJA_VERSION = 'v0.0.1'
NINJA_DESCRIPTION = """
### 点击跳转 -> [NinjaXia](https://gitee.com/wu_cl/NinjaXia)
"""
NINJA_DOCS_URL = '/docs'
NINJA_OPENAPI_URL = '/openapi'
NINJA_CSRF = False

# Uvicorn
UVICORN_HOST = '127.0.0.1'
UVICORN_PORT = 8000
UVICORN_RELOAD = True

# PATH
LOG_PATH = BASE_DIR / 'xia' / 'logs'
REPORT_PATH = BASE_DIR / 'templates' / 'report.html'
SERVER_REPORT_PATH = 'https://XXX.XXX.COM/v1/api_test_reports/{pk}/detail?page=1&size=10'

# Token
TOKEN_ALGORITHM: str = 'HS256'
TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # token 时效 60 * 24 * 1 = 1 天

# Task
TASK_REDIS_HOST = '127.0.0.1'
TASK_REDIS_PORT = 6379
TASK_REDIS_PASSWORD = ''
TASK_REDIS_DATABASE = 1
TASK_REDIS_TIMEOUT = 5
TASK_TP_STATUS = True
TASK_PP_EXECUTOR_MAX_WORKERS = 10
TASK_PP_STATUS = True
TASK_TP_EXECUTOR_MAX_WORKERS = 10
TASK_COALESCE = False
TASK_MAX_INSTANCES = 1
