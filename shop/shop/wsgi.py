"""
WSGI config for shop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

# import sys
#
# # add the hellodjango project path into the sys.path
# sys.path.append('/home/nazar/shop1/work/shop')
#
# # add the virtualenv site-packages path to the sys.path
# sys.path.append('/home/nazar/shop1/lib/site-packages')
#
# # poiting to the project settings
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop.settings")


from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop.settings")

application = get_wsgi_application()
