"""
WSGI config for daaggregator project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys
import site

from django.core.wsgi import get_wsgi_application

site.addsitedir("/home/rey44/da-tool/venv/lib/python3.5/site-packages")

sys.path.append("/home/rey44/da-tool/framework-side/daaggregator")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "daaggregator.settings")

activate_env = os.path.expanduser("/home/rey44/da-tool/venv/bin/activate_this.py")
exec(open(activate_env, "r").read(), dict(__file__=activate_env))

#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()

application = get_wsgi_application()
