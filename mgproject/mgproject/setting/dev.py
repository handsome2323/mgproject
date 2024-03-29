"""
Django settings for mgproject project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import django
import os, sys
import reprlib
import re

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.conf import global_settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 打印我们的打包路径
# print(sys.path)
#添加打包路径
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^pv$=nyc#brz(j_8nxya6v=dy7*bt9ihyn_jwdeay$!#x6n-d_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['www.nagle.cn','127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'userapp', #用户模块子应用
    'newsapp',#新闻模块子应用
    'verifications',#验证码模块子应用
    'oauth',#qq登录子模块
    'haystack', # 全⽂检索
    'payment',#支付子应用
    'django_crontab',#定时任务
    'dingding',#钉钉登录子模块
    'rest_framework'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'md1.md1'
]
WSGI_APPLICATION = 'api.wsgi.application'
ROOT_URLCONF = 'mgproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        # jinja2模板引擎
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'newsapp.mycontext.get_channels'
            ],
            # 补充Jinja2模板引擎环境
            'environment': 'mgproject.utils.jinja2_env.environment',
        },
    },

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

WSGI_APPLICATION = 'mgproject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mgdb',
        'USER': 'xiaolin',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS=[

    os.path.join(BASE_DIR,'static')
]
print('STATICFILES_DIRS',STATICFILES_DIRS)

# 配置Redis数据库
CACHES = {
 "default": { # 默认
 "BACKEND": "django_redis.cache.RedisCache",
 "LOCATION": "redis://192.168.0.104:6379/0",
 "OPTIONS": {
 "CLIENT_CLASS": "django_redis.client.DefaultClient",
 }
 },
 "session": { # session
 "BACKEND": "django_redis.cache.RedisCache",
 "LOCATION": "redis://127.0.0.1/1",
 "OPTIONS": {
 "CLIENT_CLASS": "django_redis.client.DefaultClient",
 }
 },
 "verify_code": { # 验证码
 "BACKEND": "django_redis.cache.RedisCache",
 "LOCATION": "redis://127.0.0.1/2",
 "OPTIONS": {
 "CLIENT_CLASS": "django_redis.client.DefaultClient",
 }
 },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# 配置项⽬⽇志
LOGGING = {
 'version': 1,
 'disable_existing_loggers': False, # 是否禁⽤已经存在的⽇志器
 'formatters': { # ⽇志信息显示的格式
 'verbose': {
 'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
 },
 'simple': {
 'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
 },
 },
 'filters': { # 对⽇志进⾏过滤
 'require_debug_true': { # django在debug模式下才输出⽇志
 '()': 'django.utils.log.RequireDebugTrue',
 },
 },
 'handlers': { # ⽇志处理⽅法
 'console': { # 向终端中输出⽇志
 'level': 'INFO',
 'filters': ['require_debug_true'],
 'class': 'logging.StreamHandler',
 'formatter': 'simple'
 },
 'file': { # 向⽂件中输出⽇志
 'level': 'INFO',
 'class': 'logging.handlers.RotatingFileHandler',
 'filename': os.path.join(os.path.dirname(BASE_DIR),'logs/mangguo.log'), # ⽇志⽂件的位置
 'maxBytes': 300 * 1024 * 1024,
 'backupCount': 10,
 'formatter': 'verbose'
 },
 },
 'loggers': { # ⽇志器
 'django': { # 定义了⼀个名为django的⽇志器
 'handlers': ['console', 'file'],
     # 可以同时向终端与⽂件中输出⽇志
 'propagate': True, # 是否继续传递⽇志信息
 'level': 'INFO', # ⽇志器接收的最低⽇志级别
 },
 }
}

#添加自定义模型类(应用名.模型类名)
AUTH_USER_MODEL = 'userapp.User'

# 配置短信验证码参数（互亿无线平台）
APIID = 'C94207158'

APIKEY='28e5fd057d064092bd5ce0e36414379f'

# 指定自定义认证类路径
AUTHENTICATION_BACKENDS = ['userapp.auth.MutiAccountLoginAuth']

# #指定登录首页请求地址
LOGIN_URL='/login/'

# QQ登录的配置参数
QQ_CLIENT_ID='101917966'

QQ_REDIRECT_URI = 'http://www.nagle.cn:8000/about' # 回调地址


QQ_APP_KEY = '20fcc768255829c08fa4efbe8acf0001' # app key

# 文件存储类相关配置
DEFAULT_FILE_STORAGE = 'mgproject.utils.fastdfs.fdfs_storage.FastDFSStorage'
FDFS_BASE_URL = 'http://192.168.226.134:8888/'

# Haystack
HAYSTACK_CONNECTIONS = {
 'default': {
 'ENGINE':
'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine'
,
 'URL': 'http://192.168.180.1:9200/', # Elasticsearch服务器ip地址，端⼝号固定为9200
 'INDEX_NAME': 'mangguo_indexes', # Elasticsearch建⽴的索引库的名称
 },
}

# 支付宝支付配置
ALIPAY_APPID = '2021000118684756'
ALIPAY_DEBUG = True
ALIPAY_URL = 'https://openapi.alipaydev.com/gateway.do?'
ALIPAY_RETURN_URL = 'http://127.0.0.1:8000/payment/status/'

#定时任务相关配置
CRONJOBS = [
 # 每1分钟⽣成⼀次⾸⻚静态⽂件
 ('*/1 * * * *',
'newsapp.static_index.generate_static_index_html', '>' +
os.path.join(BASE_DIR, 'logs/crontab.log'))
]
print(CRONJOBS)
# 解决 crontab 中⽂问题
CRONTAB_COMMAND_PREFIX = 'LANG_ALL=zh_cn.UTF-8'
