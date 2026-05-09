import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visitor_system.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Profile

if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser('admin', 'admin@nile.edu.ng', 'admin123')
    # Signal auto-creates profile, so we just update it
    profile = user.profile
    profile.dept = 'Security Unit'
    profile.save()
    print("Superuser 'admin' created successfully with password 'admin123' and assigned to Security Unit.")
else:
    print("Superuser 'admin' already exists.")
