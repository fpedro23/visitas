"""
WSGI config for visitas project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
import os
import sys
import site

os.environ['PYTHON_EGG_CACHE'] = '/eggCache'


# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/sisefenlin/visitas/ve/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/home/sisefenlin/visitas')
sys.path.append('/home/sisefenlin/visitas/visitas_stg')

# Activate your virtual env
#activate_env = os.path.expanduser("/home/sisefenlin/visitas/ve/bin/activate_this.py")
#execfile(activate_env, dict(__file__=activate_env))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "visitas.settings")
#os.environ["DJANGO_SETTINGS_MODULE"] = "visitas.settings"
#os.environ["DJANGO_SETTINGS_MODULE"] = "{{ project_name }}.settings"

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
