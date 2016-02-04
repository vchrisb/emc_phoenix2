from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
	print("------ creating admin------")
    User.objects.create_superuser('admin', 'admin@domain.local', 'admin')
