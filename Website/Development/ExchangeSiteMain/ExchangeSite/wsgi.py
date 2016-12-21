import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('~/.virtualenvs/bitsomething/local/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/home/Programming/Website')
sys.path.append('/home/Programming/Website/ExchangeSiteMain')
sys.path.append('/home/Programming/Website/ExchangeSiteMain/ExchangeSite')

os.environ['DJANGO_SETTINGS_MODULE'] = 'ExchangeSite.settings.MainSettings'

# Activate your virtual env
# Linux
# activate_env=os.path.expanduser("~/.virtualenvs/bitsomething/bin/activate_this.py")
# Windows
activate_env=os.path.expanduser("~/Envs/bitsomething/Scripts/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
