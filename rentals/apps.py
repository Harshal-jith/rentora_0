from django.apps import AppConfig
from django.db.models.signals import post_migrate

def ensure_temp_user(sender, **kwargs):
    from django.contrib.auth.models import User
    try:
        u, created = User.objects.get_or_create(
            username='user@gmail.com',
            defaults={'email': 'user@gmail.com', 'is_active': True}
        )
        u.set_password('password')
        u.email = 'user@gmail.com'
        u.is_active = True
        u.save()

        u2, created2 = User.objects.get_or_create(
            username='user',
            defaults={'email': 'user@gmail.com', 'is_active': True}
        )
        u2.set_password('password')
        u2.email = 'user@gmail.com'
        u2.is_active = True
        u2.save()
    except Exception as e:
        print(f"Auto temp user check note: {e}")

class RentalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rentals'

    def ready(self):
        post_migrate.connect(ensure_temp_user, sender=self)
