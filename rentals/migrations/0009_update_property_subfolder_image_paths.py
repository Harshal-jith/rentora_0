from django.db import migrations

def update_property_images(apps, schema_editor):
    Property = apps.get_model('rentals', 'Property')
    
    slug_to_folder = {
        'wayanad-mistwood-sanctuary-estate': ('prop_01', 4),
        'munnar-celestial-tea-haven-manor': ('prop_02', 3),
        'varkala-azure-cliffside-ocean-residence': ('prop_03', 3),
        'kumarakom-lotus-lakefront-pavilion': ('prop_04', 3),
        'alleppey-sovereign-backwater-villa': ('prop_05', 3),
        'vagamon-pine-ridge-mountain-retreat': ('prop_06', 3),
        'kovalam-horizon-oceanfront-reserve': ('prop_07', 3),
        'fort-kochi-maritime-heritage-manor': ('prop_08', 3),
        'athirappilly-canopy-waterfall-estate': ('prop_09', 3),
        'thekkady-spice-plantation-heritage-manor': ('prop_10', 3),
        'idukki-mountain-ridge-glass-pavilion': ('prop_11', 3),
        'kannur-malabar-cliffside-heritage-residence': ('prop_12', 3),
    }

    for prop in Property.objects.all():
        folder_info = slug_to_folder.get(prop.slug)
        if folder_info:
            folder, img_count = folder_info
            main_img = f"/static/images/properties/{folder}/{folder}_img_1.jpg"
            gallery = [f"/static/images/properties/{folder}/{folder}_img_{i}.jpg" for i in range(1, img_count + 1)]
            
            prop.main_image = main_img
            prop.gallery_json = gallery
            prop.save()

class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0008_userprofile'),
    ]

    operations = [
        migrations.RunPython(update_property_images, reverse_code=migrations.RunPython.noop),
    ]
