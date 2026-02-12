import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')
django.setup()

from news_app.models import CustomUser

print("Current Users and Roles:")
for user in CustomUser.objects.all():
    groups = ", ".join([g.name for g in user.groups.all()])
    print(f"{user.username:15} | Role: {user.role:10} | Groups: {groups}")
