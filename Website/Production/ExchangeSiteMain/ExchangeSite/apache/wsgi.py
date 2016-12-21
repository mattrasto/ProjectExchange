import os
import sys
import site

# Attempts to force-set PYTHONPATH to expected value
'''
sys.path = ['', '/home/mal/.virtualenvs/bitsomething/lib/python2.7', '/home/mal/.virtualenvs/bitsomething/lib/python2.7/plat-x86_64-linux-gnu', 
            '/home/mal/.virtualenvs/bitsomething/lib/python2.7/lib-tk', '/home/mal/.virtualenvs/bitsomething/lib/python2.7/lib-old', 
            '/home/mal/.virtualenvs/bitsomething/lib/python2.7/lib-dynload', '/usr/lib/python2.7', '/usr/lib/python2.7/plat-x86_64-linux-gnu', '/usr/lib/python2.7/lib-tk', 
            '/home/mal/.virtualenvs/bitsomething/local/lib/python2.7/site-packages', '/home/mal/.virtualenvs/bitsomething/lib/python2.7/site-packages']
'''

# Restores system PYTHONPATH
'''
sys.path = ['', '/home/mal/Programming/Website/Production/ExchangeSiteMain/ExchangeSite', '/home/mal/.virtualenvs/bitsomething/lib/python2.7/site-packages', 
            '/usr/lib/python2.7', '/usr/lib/python2.7/plat-x86_64-linux-gnu', '/usr/lib/python2.7/lib-tk','/usr/lib/python2.7/lib-old', '/usr/lib/python2.7/lib-dynload', 
            '/usr/local/lib/python2.7/dist-packages', '/usr/lib/python2.7/dist-packages', '/usr/lib/python2.7/dist-packages/PILcompat', '/usr/lib/python2.7/dist-packages/gtk-2.0', 
            '/usr/lib/python2.7/dist-packages/ubuntu-sso-client', '/home/mal/.virtualenvs/bitsomething/local/lib/python2.7/site-packages', '/home/mal/Programming/Website/Production/', 
            '/home/mal/Programming/Website/Production/ExchangeSiteMain/', '/home/mal/Programming/Website/Production/ExchangeSiteMain/ExchangeSite']
'''

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/mal/.virtualenvs/bitsomething/local/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/home/mal/Programming/Website/Production/')
sys.path.append('/home/mal/Programming/Website/Production/ExchangeSiteMain/')
sys.path.append('/home/mal/Programming/Website/Production/ExchangeSiteMain/ExchangeSite')

# Activate virtual environment (Method 1)
activate_env = os.path.expanduser("/home/mal/.virtualenvs/bitsomething/bin/activate_this.py")
#activate_env = '/home/mal/.virtualenvs/bitsomething/bin/python2.7'
INTERP = execfile(activate_env, dict(__file__=activate_env))

# Activate virtual environment (Method 2)
#virtualenv_root = '/home/mal/.virtualenvs/bitsomething'
#INTERP = os.path.join(virtualenv_root, 'bin', 'python')

import mod_wsgi
import django

print ""
print "-----SETTINGS-----"
print "mod_wsgi Version: " + str(mod_wsgi.version)
print "Process Group: " + str(mod_wsgi.process_group)
print "Application Group: " + str(mod_wsgi.application_group)
print "Django Version: " + str(django.VERSION)
print "Django Directory: " + str(django.__file__)
print "Python Virtual Environment Interpreter Directory: " + str(INTERP)
print "Python Current Interpreter Directory: " + str(sys.executable)
print "Python Version: " + str(sys.version)
print "Python Prefix: " + str(sys.prefix)

print ""
print "-----START SYSTEM PYTHONPATH-----"
for path in sys.path:
    print path
print "-----END SYSTEM PYTHONPATH-----"
print ""

os.environ['DJANGO_SETTINGS_MODULE'] = 'ExchangeSite.MainSettings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
