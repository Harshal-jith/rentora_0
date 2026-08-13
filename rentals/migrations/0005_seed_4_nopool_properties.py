from django.db import migrations

NO_POOL_PROPERTIES = [
    {
        "title": "Athirappilly Canopy Waterfall Estate",
        "slug": "athirappilly-canopy-waterfall-estate",
        "location": "athirappilly",
        "location_display_name": "Chalakudy Rainforest, Athirappilly",
        "property_type": "villa",
        "price_per_night": 44000,
        "bedrooms": 4,
        "bathrooms": 4,
        "max_guests": 8,
        "short_description": "Biophilic luxury rainforest villa suspended in the jungle canopy with a cantilevered wooden observatory deck overlooking Athirappilly Waterfalls.",
        "description": "Immerse yourself in untouched nature at Athirappilly Canopy Waterfall Estate. Suspended in the ancient rainforest canopy of Chalakudy, this biophilic luxury pavilion features dark teak timber, black steel framing, and double-height glass walls. Step onto a cantilevered wooden treehouse deck built around giant tropical trees, listening to the roar of Athirappilly Waterfalls. No swimming pool — pure natural rainforest immersion.",
        "main_image": "/static/images/properties/prop_09_athirappilly.jpg",
        "gallery_json": [
            "/static/images/properties/prop_09_athirappilly.jpg"
        ],
        "amenities_json": [
            "Cantilevered Treehouse Observatory Deck", "Direct Waterfall View Terrace", "Private Naturalist & Guided Treks", 
            "Organic Forest-to-Table Dining", "Heated Jacuzzi Suite", "High-speed Starlink WiFi", 
            "Acoustic Sound-Proofing", "Air Conditioning"
        ],
        "rating": 4.97,
        "reviews_count": 24,
        "is_featured": True
    },
    {
        "title": "Thekkady Spice Plantation Heritage Manor",
        "slug": "thekkady-spice-plantation-heritage-manor",
        "location": "thekkady",
        "location_display_name": "Periyar Spice Sanctuary, Thekkady",
        "property_type": "estate",
        "price_per_night": 39000,
        "bedrooms": 5,
        "bathrooms": 5,
        "max_guests": 10,
        "short_description": "Grand colonial spice plantation manor set within 80 acres of organic cardamom and pepper gardens with stone fire pit and timber tea pavilion.",
        "description": "Surrounded by 80 acres of fragrant organic cardamom, vanilla, and pepper plantations in Periyar, Thekkady Spice Manor offers timeless highland serenity. Constructed from local granite masonry and rosewood timber, it features wide wraparound verandas, stone garden pathways, an outdoor sunken fire pit, and an open-air tea tasting pavilion. No swimming pool — private plantation sanctuary.",
        "main_image": "/static/images/properties/prop_10_thekkady.jpg",
        "gallery_json": [
            "/static/images/properties/prop_10_thekkady.jpg"
        ],
        "amenities_json": [
            "80-Acre Private Spice Plantation", "Outdoor Stone Fire Pit Seating", "Open-Air Timber Tea Pavilion", 
            "Private Master Chef", "Guided Spice Tasting Walks", "Stone Fireplace Lounge", 
            "High-speed Fiber WiFi", "Helipad Transfer Available"
        ],
        "rating": 4.95,
        "reviews_count": 29,
        "is_featured": True
    },
    {
        "title": "Idukki Mountain Ridge Glass Pavilion",
        "slug": "idukki-mountain-ridge-glass-pavilion",
        "location": "idukki",
        "location_display_name": "High Range Ridge, Idukki",
        "property_type": "bungalow",
        "price_per_night": 35000,
        "bedrooms": 3,
        "bathrooms": 3,
        "max_guests": 6,
        "short_description": "Modernist glass mountain pavilion perched high over Idukki's misty valleys with sunken stone fire pit deck and stargazing terrace.",
        "description": "Standing proudly on a high-altitude mountain ridge in Idukki, this glass pavilion offers 360-degree views of misty valleys and mountain peaks. Built with dark grey basalt stone masonry, cedar timber ceilings, and floor-to-ceiling glass, it features a sunken outdoor stone fire pit and an upper-deck stargazing lounge. No swimming pool — mountain ridge retreat.",
        "main_image": "/static/images/properties/prop_11_idukki.jpg",
        "gallery_json": [
            "/static/images/properties/prop_11_idukki.jpg"
        ],
        "amenities_json": [
            "Upper Deck Stargazing Lounge", "Sunken Outdoor Fire Pit Deck", "Panoramic Mountain Valley Views", 
            "Basalt Stone Fireplace", "Private Highland Chef", "High-speed Starlink WiFi", 
            "Heated Floor Suites", "Daily Housekeeping"
        ],
        "rating": 4.98,
        "reviews_count": 18,
        "is_featured": True
    },
    {
        "title": "Kannur Malabar Cliffside Heritage Residence",
        "slug": "kannur-malabar-cliffside-heritage-residence",
        "location": "kannur",
        "location_display_name": "Payyambalam Cliff Headland, Kannur",
        "property_type": "bungalow",
        "price_per_night": 37000,
        "bedrooms": 4,
        "bathrooms": 4,
        "max_guests": 8,
        "short_description": "Refined coastal heritage bungalow on Malabar cliffs with whitewashed laterite walls, terracotta roofs, and cliffside ocean-view gardens.",
        "description": "Perched on Kannur's red laterite headland along the pristine Malabar coastline, this heritage residence blends classic colonial architecture with oceanfront luxury. Featuring whitewashed laterite masonry, clay terracotta tiled roofs, carved teakwood pillars, and deep shaded verandas overlooking cliffside gardens and sunset waves. No swimming pool — cliffside oceanfront gardens.",
        "main_image": "/static/images/properties/prop_12_kannur.jpg",
        "gallery_json": [
            "/static/images/properties/prop_12_kannur.jpg"
        ],
        "amenities_json": [
            "Unobstructed Malabar Sea Views", "Private Cliffside Ocean Gardens", "Traditional Theyyam Performance Access", 
            "Private Coastal Chef", "Ayurvedic Wellness Massages", "Shaded Teak Verandas", 
            "High-Speed Fiber WiFi", "24/7 Butler Service"
        ],
        "rating": 4.96,
        "reviews_count": 21,
        "is_featured": True
    }
]

def seed_nopool_properties(apps, schema_editor):
    Property = apps.get_model('rentals', 'Property')
    for data in NO_POOL_PROPERTIES:
        Property.objects.update_or_create(
            slug=data['slug'],
            defaults=data
        )

def reverse_func(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0004_seed_phase1_properties'),
    ]

    operations = [
        migrations.RunPython(seed_nopool_properties, reverse_code=reverse_func),
    ]
