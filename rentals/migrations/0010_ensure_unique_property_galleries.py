from django.db import migrations

def update_property_galleries(apps, schema_editor):
    Property = apps.get_model('rentals', 'Property')
    
    slug_to_folder = {
        'wayanad': ('prop_01', 4),
        'munnar': ('prop_02', 3),
        'varkala': ('prop_03', 3),
        'kumarakom': ('prop_04', 3),
        'alleppey': ('prop_05', 3),
        'vagamon': ('prop_06', 3),
        'kovalam': ('prop_07', 3),
        'fort_kochi': ('prop_08', 3),
        'athirappilly': ('prop_09', 3),
        'thekkady': ('prop_10', 3),
        'idukki': ('prop_11', 3),
        'kannur': ('prop_12', 3),
    }

    for prop in Property.objects.all():
        folder_info = None
        for key, val in slug_to_folder.items():
            if key in prop.slug or key in prop.location:
                folder_info = val
                break
        
        if folder_info:
            folder, count = folder_info
            prop.main_image = f"/static/images/properties/{folder}/{folder}_img_1.jpg"
            prop.gallery_json = [f"/static/images/properties/{folder}/{folder}_img_{i}.jpg" for i in range(1, count + 1)]
            prop.save()

class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0009_update_property_subfolder_image_paths'),
    ]

    operations = [
        migrations.RunPython(update_property_galleries, reverse_code=migrations.RunPython.noop),
    ]
