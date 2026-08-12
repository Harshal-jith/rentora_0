from django.db import migrations

def create_default_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')

    # 1. Ensure temporary normal user exists: user / password
    try:
        user_obj, created = User.objects.get_or_create(
            username='user',
            defaults={'email': 'user@rentora.in'}
        )
        user_obj.set_password('password')
        user_obj.is_staff = False
        user_obj.is_superuser = False
        user_obj.save()
    except Exception:
        pass

    # 2. Ensure superuser exists: admin / RentoraAdmin2026!
    try:
        admin_obj, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@rentora.in'}
        )
        admin_obj.set_password('RentoraAdmin2026!')
        admin_obj.is_staff = True
        admin_obj.is_superuser = True
        admin_obj.save()
    except Exception:
        pass

def reverse_func(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0002_inquiry_ip_address_visitorlog'),
    ]

    operations = [
        migrations.RunPython(create_default_users, reverse_code=reverse_func),
    ]
