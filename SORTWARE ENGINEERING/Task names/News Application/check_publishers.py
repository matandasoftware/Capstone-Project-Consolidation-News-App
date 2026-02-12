import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')
django.setup()

from news_app.models import Publisher, CustomUser

print("Publishers (Organizations):")
publishers = Publisher.objects.all()
if publishers:
    for pub in publishers:
        print(f"{pub.name}")
        print(f"  Editors: {', '.join([e.username for e in pub.editors.all()])}")
        print(f"  Journalists: {', '.join([j.username for j in pub.journalists.all()])}")
else:
    print("No publishers exist yet.")

print("\nUsers with EDITOR role:")
editors = CustomUser.objects.filter(role='EDITOR')
for editor in editors:
    print(f"{editor.username}")
