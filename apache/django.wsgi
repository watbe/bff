import os
import sys

sys.stderr.write('\n'.join(sys.path))

path = '/home/bff/bff_dev/src'
if path not in sys.path:
	sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'bff.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
