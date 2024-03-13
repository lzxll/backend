import os
import sys
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ================================================= #
# ******************** 动态配置 ******************** #
# ================================================= #

from conf.env import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure--z8%exyzt7e_%i@1+#1mm=%lb5=^fx_57=1@a+_y7bg5-w%)sm"
# 初始化plugins插件路径到环境变量中
PLUGINS_PATH = os.path.join(BASE_DIR, "plugins")
sys.path.insert(0, os.path.join(PLUGINS_PATH))

[
    sys.path.insert(0, os.path.join(PLUGINS_PATH, ele))
    for ele in os.listdir(PLUGINS_PATH)
    if os.path.isdir(os.path.join(PLUGINS_PATH, ele)) and not ele.startswith("__")
]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = locals().get("DEBUG", True)
ALLOWED_HOSTS = locals().get("ALLOWED_HOSTS", ["*"])

# 列权限需要排除的App应用
COLUMN_EXCLUDE_APPS = ['channels', 'captcha'] + locals().get("COLUMN_EXCLUDE_APPS", [])

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_comment_migrate",
    "rest_framework",
    "django_filters",
    "corsheaders",  # 注册跨域app
    "drf_yasg",
    "captcha",
    "channels",
    "dvadmin.system",
]

MIDDLEWARE = [
    "dvadmin.utils.middleware.HealthCheckMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # 跨域中间件
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "dvadmin.utils.middleware.ApiLoggingMiddleware",
]

ROOT_URLCONF = "application.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "application.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": DATABASE_ENGINE,
        "NAME": DATABASE_NAME,
        "USER": DATABASE_USER,
        "PASSWORD": DATABASE_PASSWORD,
        "HOST": DATABASE_HOST,
        "PORT": DATABASE_PORT,
    }
}
AUTH_USER_MODEL = "system.Users"
USERNAME_FIELD = "username"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
# # 设置django的静态文件目录
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_ROOT = "media"  # 项目下的目录
MEDIA_URL = "/media/"  # 跟STATIC_URL类似，指定用户可以通过这个url找到文件

#添加以下代码以后就不用写{% load staticfiles %}，可以直接引用
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
)
# 收集静态文件，必须将 MEDIA_ROOT,STATICFILES_DIRS先注释
# python manage.py collectstatic
# STATIC_ROOT=os.path.join(BASE_DIR,'static')

# ================================================= #
# ******************* 跨域的配置 ******************* #
# ================================================= #

# 全部允许配置
CORS_ORIGIN_ALLOW_ALL = True
# 允许cookie
CORS_ALLOW_CREDENTIALS = True  # 指明在跨域访问中，后端是否支持对cookie的操作

# ===================================================== #
# ********************* channels配置 ******************* #
# ===================================================== #
ASGI_APPLICATION = 'application.asgi.application'
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [('127.0.0.1', 6379)], #需修改
#         },
#     },
# }


# ================================================= #
# ********************* 日志配置 ******************* #
# ================================================= #
# # log 配置部分BEGIN #
SERVER_LOGS_FILE = os.path.join(BASE_DIR, "logs", "server.log")
ERROR_LOGS_FILE = os.path.join(BASE_DIR, "logs", "error.log")
LOGS_FILE = os.path.join(BASE_DIR, "logs")
if not os.path.exists(os.path.join(BASE_DIR, "logs")):
    os.makedirs(os.path.join(BASE_DIR, "logs"))

# 格式:[2020-04-22 23:33:01][micoservice.apps.ready():16] [INFO] 这是一条日志:
# 格式:[日期][模块.函数名称():行号] [级别] 信息
STANDARD_LOG_FORMAT = (
    "[%(asctime)s][%(name)s.%(funcName)s():%(lineno)d] [%(levelname)s] %(message)s"
)
CONSOLE_LOG_FORMAT = (
    "[%(asctime)s][%(name)s.%(funcName)s():%(lineno)d] [%(levelname)s] %(message)s"
)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": STANDARD_LOG_FORMAT},
        "console": {
            "format": CONSOLE_LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "file": {
            "format": CONSOLE_LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": SERVER_LOGS_FILE,
            "maxBytes": 1024 * 1024 * 100,  # 100 MB
            "backupCount": 5,  # 最多备份5个
            "formatter": "standard",
            "encoding": "utf-8",
        },
        "error": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": ERROR_LOGS_FILE,
            "maxBytes": 1024 * 1024 * 100,  # 100 MB
            "backupCount": 3,  # 最多备份3个
            "formatter": "standard",
            "encoding": "utf-8",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "console",
        },

    },
    "loggers": {
        "": {
            "handlers": ["console", "error", "file"],
            "level": "INFO",
        },
        "django": {
            "handlers": ["console", "error", "file"],
            "level": "INFO",
            "propagate": False,
        },
        'django.db.backends': {
            'handlers': ["console", "error", "file"],
            'propagate': False,
            'level': "INFO"
        },
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["console", "error", "file"],
        },
        "uvicorn.access": {
            "handlers": ["console", "error", "file"],
            "level": "INFO"
        },
    },
}

# ================================================= #
# *************** REST_FRAMEWORK配置 *************** #
# ================================================= #

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",  # 日期时间格式配置
    "DATE_FORMAT": "%Y-%m-%d",
    "DEFAULT_FILTER_BACKENDS": (
        # 'django_filters.rest_framework.DjangoFilterBackend',
        "dvadmin.utils.filters.CustomDjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "dvadmin.utils.pagination.CustomPagination",  # 自定义分页
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",  # 只有经过身份认证确定用户身份才能访问
    ],
    "EXCEPTION_HANDLER": "dvadmin.utils.exception.CustomExceptionHandler",  # 自定义的异常处理
}
# ================================================= #
# ******************** 登录方式配置 ******************** #
# ================================================= #

AUTHENTICATION_BACKENDS = ["dvadmin.utils.backends.CustomBackend"]
# ================================================= #
# ****************** simplejwt配置 ***************** #
# ================================================= #
SIMPLE_JWT = {
    # token有效时长
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=1440),
    # token刷新后的有效时间
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    # 设置前缀
    "AUTH_HEADER_TYPES": ("JWT",),
    "ROTATE_REFRESH_TOKENS": True,
}

# ====================================#
# ****************swagger************#
# ====================================#
SWAGGER_SETTINGS = {
    # 基础样式
    "SECURITY_DEFINITIONS": {"basic": {"type": "basic"}},
    # 如果需要登录才能够查看接口文档, 登录的链接使用restframework自带的.
    "LOGIN_URL": "apiLogin/",
    # 'LOGIN_URL': 'rest_framework:login',
    "LOGOUT_URL": "rest_framework:logout",
    # 'DOC_EXPANSION': None,
    # 'SHOW_REQUEST_HEADERS':True,
    # 'USE_SESSION_AUTH': True,
    # 'DOC_EXPANSION': 'list',
    # 接口文档中方法列表以首字母升序排列
    "APIS_SORTER": "alpha",
    # 如果支持json提交, 则接口文档中包含json输入框
    "JSON_EDITOR": True,
    # 方法列表字母排序
    "OPERATIONS_SORTER": "alpha",
    "VALIDATOR_URL": None,
    "AUTO_SCHEMA_TYPE": 2,  # 分组根据url层级分，0、1 或 2 层
    "DEFAULT_AUTO_SCHEMA_CLASS": "dvadmin.utils.swagger.CustomSwaggerAutoSchema",
}

# ================================================= #
# **************** 验证码配置  ******************* #
# ================================================= #
CAPTCHA_IMAGE_SIZE = (160, 46)  # 设置 captcha 图片大小
CAPTCHA_LENGTH = 4  # 字符个数
CAPTCHA_TIMEOUT = 1  # 超时(minutes)
CAPTCHA_OUTPUT_FORMAT = "%(image)s %(text_field)s %(hidden_field)s "
CAPTCHA_FONT_SIZE = 36  # 字体大小
CAPTCHA_FOREGROUND_COLOR = "#64DAAA"  # 前景色
CAPTCHA_BACKGROUND_COLOR = "#F5F7F4"  # 背景色
CAPTCHA_NOISE_FUNCTIONS = (
    "captcha.helpers.noise_arcs",  # 线
    # "captcha.helpers.noise_dots",  # 点
)
# CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge' #字母验证码
CAPTCHA_CHALLENGE_FUNCT = "captcha.helpers.math_challenge"  # 加减乘除验证码

# ================================================= #
# ******************** 其他配置 ******************** #
# ================================================= #

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
API_LOG_ENABLE = True
# API_LOG_METHODS = 'ALL' # ['POST', 'DELETE']
API_LOG_METHODS = ["POST", "UPDATE", "DELETE", "PUT"]  # ['POST', 'DELETE']
API_MODEL_MAP = {
    "/token/": "登录模块",
    "/api/login/": "登录模块",
    "/api/plugins_market/plugins/": "插件市场",
}

DJANGO_CELERY_BEAT_TZ_AWARE = False
CELERY_TIMEZONE = "Asia/Shanghai"  # celery 时区问题
# 静态页面压缩
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

ALL_MODELS_OBJECTS = []  # 所有app models 对象

# 初始化需要执行的列表，用来初始化后执行
INITIALIZE_LIST = []
INITIALIZE_RESET_LIST = []
# 表前缀
TABLE_PREFIX = locals().get('TABLE_PREFIX', "")
# 系统配置
SYSTEM_CONFIG = {}
# 字典配置
DICTIONARY_CONFIG = {}

# ================================================= #
# ******************** 插件配置 ******************** #
# ================================================= #
# 租户共享app
TENANT_SHARED_APPS = []
# 插件 urlpatterns
PLUGINS_URL_PATTERNS = []
# ********** 一键导入插件配置开始 **********
# 例如:
# from dvadmin_upgrade_center.settings import *    # 升级中心
# from dvadmin_celery.settings import *            # celery 异步任务
# from dvadmin_third.settings import *            # 第三方用户管理
# from dvadmin_ak_sk.settings import *            # 秘钥管理管理
# from dvadmin_tenants.settings import *            # 租户管理
#from dvadmin_social_auth.settings import *
# ...
# ********** 一键导入插件配置结束 **********
