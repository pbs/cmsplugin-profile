INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cms',
    'cmsroles',
    'mptt',
    'filer',
    'menus',
    'sekizai',
    'cmsplugin_profile',
    'django.contrib.admin',
]

CMS_TEMPLATES = [('cms/dummy.html', 'cms/dummy.html')]
CMS_MODERATOR = True
CMS_PERMISSION = True
STATIC_ROOT = '/static/'
STATIC_URL = '/static/'
ROOT_URLCONF = 'cmsplugin_profile.tests.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': (
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
            ),
            'loaders': (
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader',
            ),
            'debug': False
        },
    },
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',  # Or path to database file if using sqlite3.
    }
}
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
SECRET_KEY = 'secret'
