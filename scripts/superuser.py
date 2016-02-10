import os, django, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "phoenix.settings")
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
	print("creating superuser 'admin'")
	User.objects.create_superuser('admin', 'admin@domain.local', 'admin')
else:
	print("superuser 'admin' exists")