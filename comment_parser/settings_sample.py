#For development environment, copy this file to settings_dev.py
#When deploying, you should copy this file to settings_prod.py, and change the
#  values accordingly.       

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    #If you need to configure a MySQL database, use the following structure:
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': '',
#        'USER': '',
#        'PASSWORD': '',
#        'HOST': '127.0.0.1',
#        'PORT': '3306'        
#    }
    #This will create a local file with a database, useful for testing   
    'default': {
        'ENGINE':'django.db.backends.sqlite3',
        'NAME':'sample.sqlite3'
    }
}

#Add the website URL or IP here
ALLOWED_HOSTS = []

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/static/'

#If you will need to specify a folder where the static files 
#  should be copied to (using 'manage.py collectstatic'),
#  set the following parameter:
#STATIC_ROOT = /path/to/static

#Data used to connect manually to the database (needed in a corner case)
GENERAL_DATA_DB_DETAILS = {
    'NAME': 'general_data',
    'USER': 'dbuser',
    'PASSWORD': 'Mh73pNuVxXKXUZZM',
    'HOST': '127.0.0.1',
    'PORT': 3306        
}

#  ______  _______  __       _______ .______     ____    ____ 
# /      ||   ____||  |     |   ____||   _  \    \   \  /   / 
#|  ,----'|  |__   |  |     |  |__   |  |_)  |    \   \/   /  
#|  |     |   __|  |  |     |   __|  |      /      \_    _/   
#|  `----.|  |____ |  `----.|  |____ |  |\  \----.   |  |     
# \______||_______||_______||_______|| _| `._____|   |__|     

#For some weird reason, this config doesn't work when declared from the settings      
#CELERY_RESULTS_BACKEND = 'django-db'
CELERY_BROKER = 'pyamqp://guest@localhost//'
CELERY_TRACK_STARTED = True