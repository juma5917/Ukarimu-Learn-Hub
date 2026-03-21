import os
import django

# Set up the Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ukarimu_core.settings")
django.setup()

from django.contrib.auth import get_user_model

def create_superuser():
    User = get_user_model()
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

    if username and password and email:
        if not User.objects.filter(username=username).exists():
            print(f"Creating superuser: {username}")
            User.objects.create_superuser(username=username, email=email, password=password)
            print("Superuser created successfully.")
        else:
            print(f"Superuser '{username}' already exists.")
    else:
        print("Skipping superuser creation: Missing DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, or DJANGO_SUPERUSER_PASSWORD.")

if __name__ == "__main__":
    create_superuser()