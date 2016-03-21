import os, django, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "phoenix.settings")
django.setup()

from django.contrib.auth.models import User
from allauth.account.models import EmailAddress

if not User.objects.filter(username='admin').exists():
	print("creating superuser 'admin'")
	user = User.objects.create_superuser('admin', 'admin@domain.local', 'admin')
	EmailAddress.objects.create(user=user,
                                    email='admin@domain.local',
                                    primary=True,
                                    verified=True)
else:
	print("superuser 'admin' exists")
