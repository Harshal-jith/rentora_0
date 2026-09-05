from django.core.management.base import BaseCommand
from rentals.models import Property

SAMPLE_PROPERTIES = [
    {
        "title": "Wayanad Mistwood Sanctuary Estate",
        "slug": "wayanad-mistwood-sanctuary-estate",
        "location": "wayanad",
        "location_display_name": "Lakkidi Rainforest, Wayanad",
        "property_type": "estate",
        "price_per_night": 45000,
        "bedrooms": 5,
        "bathrooms": 5,
        "max_guests": 10,
        "short_description": "Modern biophilic rainforest estate with dark teakwood panels, charcoal basalt stone walls, and cantilevered infinity pool overlooking misty Western Ghats.",
        "description": "Secluded in the high-altitude tropical rainforest of Lakkidi in Wayanad, Mistwood Sanctuary Estate represents the pinnacle of modern architectural luxury in harmony with nature. Constructed from local dark charcoal granite stone, dark natural teak, and charcoal aluminum glass frames, this 6,500 sq ft pavilion features a cantilevered infinity pool floating above the emerald canopy, a stone fireplace lounge, and 24/7 personal naturalist butler service.",
        "main_image": "/static/images/properties/prop_01/prop_01_img_1.jpg",
        "gallery_json": [
            "/static/images/properties/prop_01/prop_01_img_1.jpg",
            "/static/images/properties/prop_01/prop_01_img_2.jpg",
            "/static/images/properties/prop_01/prop_01_img_3.jpg",
            "/static/images/properties/prop_01/prop_01_img_4.jpg"
        ],
        "amenities_json": [
            "Cantilevered Heated Infinity Pool", "Dark Granite Fireplace Lounge", "Private Naturalist Guide", 
            "Organic Farm-to-Table Chef", "High-speed Starlink WiFi", "Panoramic Mountain Deck", 
            "Helipad Transfer Available", "Air Conditioning"
        ],
        "rating": 4.98,
        "reviews_count": 28,
        "is_featured": True
    },
    {
        "title": "Munnar Celestial Tea Haven Manor",
        "slug": "munnar-celestial-tea-haven-manor",
        "location": "munnar",
        "location_display_name": "Chithirapuram Tea Hills, Munnar",
        "property_type": "estate",
        "price_per_night": 48000,
        "bedrooms": 6,
        "bathrooms": 6,
        "max_guests": 12,
        "short_description": "Contemporary mountain tea estate manor with light-grey slate stone walls, cedar wood framing, and panoramic fire pit terrace facing tea valleys.",
        "description": "Perched 1,650 meters above sea level amidst 120 acres of private organic tea gardens in Munnar, Celestial Tea Haven Manor is a modern architectural masterpiece. Featuring light-grey slate masonry, cedar timber beams, floor-to-ceiling glass observatory windows, an outdoor sunken fire pit deck, and custom high-altitude culinary experiences prepared by private master chefs.",
        "main_image": "/static/images/properties/prop_02/prop_02_img_1.jpg",
        "gallery_json": [
            "/static/images/properties/prop_02/prop_02_img_1.jpg",
            "/static/images/properties/prop_02/prop_02_img_2.jpg",
            "/static/images/properties/prop_02/prop_02_img_3.jpg"
        ],
        "amenities_json": [
            "120-Acre Private Tea Estate", "Sunken Outdoor Fire Pit Deck", "Stone Fireplaces in Suites", 
            "Private Tea Sommelier", "Heated Outdoor Jacuzzi", "Mountain View Terrace", 
            "24/7 Personal Host", "Farm-to-Table Dining"
        ],
        "rating": 4.97,
        "reviews_count": 34,
        "is_featured": True
    },
    {
        "title": "Varkala Azure Cliffside Ocean Residence",
        "slug": "varkala-azure-cliffside-ocean-residence",
        "location": "varkala",
        "location_display_name": "North Cliff Promenade, Varkala",
        "property_type": "cottage",
        "price_per_night": 38000,
        "bedrooms": 4,
        "bathrooms": 4,
        "max_guests": 8,
        "short_description": "Minimalist oceanfront sanctuary perched on red laterite cliffs with cantilevered infinity pool and sunset yoga terrace over the Arabian Sea.",
        "description": "An architectural tour de force standing dramatically atop Varkala's famous red laterite cliffs. Crafted from raw board-formed architectural concrete, warm timber louvers, and expansive floor-to-ceiling sliding glass walls, this coastal sanctuary offers unhindered 180-degree ocean views, a cantilevered infinity pool suspended over the waves, and private stairway access to secluded cove beaches.",
        "main_image": "/static/images/properties/prop_03/prop_03_img_1.jpg",
        "gallery_json": [
            "/static/images/properties/prop_03/prop_03_img_1.jpg",
            "/static/images/properties/prop_03/prop_03_img_2.jpg",
            "/static/images/properties/prop_03/prop_03_img_3.jpg"
        ],
        "amenities_json": [
            "180° Unobstructed Arabian Sea View", "Cliffside Cantilevered Infinity Pool", "Private Ocean Access Staircase", 
            "Glass Yoga Terrace", "Ayurvedic Spa Consultation", "Fresh Seafood Grill Master", 
            "Sonos Sound System", "Air Conditioning"
        ],
        "rating": 4.95,
        "reviews_count": 22,
        "is_featured": True
    },
    {
        "title": "Kumarakom Lotus Lakefront Pavilion",
        "slug": "kumarakom-lotus-lakefront-pavilion",
        "location": "kumarakom",
        "location_display_name": "Vembanad Lake Shoreline, Kumarakom",
        "property_type": "villa",
        "price_per_night": 42000,
        "bedrooms": 4,
        "bathrooms": 5,
        "max_guests": 8,
        "short_description": "Refined lakeside tropical estate with exposed red laterite brickwork, teak pillars, private lap pool, and timber boat dock on Lake Vembanad.",
        "description": "Situated on the peaceful lotus-covered shore of Lake Vembanad in Kumarakom, this luxury tropical pavilion blends classical Kerala craft with modern elegance. Featuring exposed warm red laterite brick walls, handcrafted teakwood pillars, deep shaded verandas, a stone lap pool, and a private timber jetty with a classic wooden boat for private lake cruises at sunset.",
        "main_image": "/static/images/properties/prop_04/prop_04_img_1.jpg",
        "gallery_json": [
            "/static/images/properties/prop_04/prop_04_img_1.jpg",
            "/static/images/properties/prop_04/prop_04_img_2.jpg",
            "/static/images/properties/prop_04/prop_04_img_3.jpg"
        ],
        "amenities_json": [
            "Private Lake Vembanad Jetty", "Lakeside Lap Pool", "Private Sunset Boat Cruiser", 
            "In-Villa Gourmet Chef", "Ayurvedic Massage Pavilion", "Tropical Garden Courtyard", 
            "High-speed Fiber WiFi", "24/7 Butler Service"
        ],
        "rating": 4.99,
        "reviews_count": 19,
        "is_featured": True
    },
    {
        "title": "Alleppey Sovereign Backwater Villa",
        "slug": "alleppey-sovereign-backwater-villa",
        "location": "alleppey",
        "location_display_name": "Punnamada Lagoon, Alleppey",
        "property_type": "villa",
        "price_per_night": 36000,
        "bedrooms": 3,
        "bathrooms": 4,
        "max_guests": 6,
        "short_description": "Sleek tropical waterfront villa with white concrete overhangs, teak slatted screens, private infinity pool, and private lagoon cruiser dock.",
        "description": "Located directly along Alleppey's quiet backwater palm channels, Sovereign Backwater Villa features sleek architectural white concrete overhangs, teak timber slatted screening, and floor-to-ceiling glass sliding panels. Relax in a private infinity pool that merges seamlessly into emerald lagoon waters, or embark on private backwater excursions from your private dock.",
        "main_image": "/static/images/properties/prop_05/prop_05_img_1.jpg",
        "gallery_json": [
            "/static/images/properties/prop_05/prop_05_img_1.jpg",
            "/static/images/properties/prop_05/prop_05_img_2.jpg",
            "/static/images/properties/prop_05/prop_05_img_3.jpg"
        ],
        "amenities_json": [
            "Lagoon-Edge Infinity Pool", "Private Dock & Wooden Cruiser", "Personal Butler & Culinary Host", 
            "Sunset Kayaking Fleet", "Air Conditioning", "High-speed WiFi", 
            "Organic Kerala Dining", "Daily Housekeeping"
        ],
        "rating": 4.96,
        "reviews_count": 31,
        "is_featured": True
    },
    {
        "title": "Vagamon Pine Ridge Mountain Retreat",
        "slug": "vagamon-pine-ridge-mountain-retreat",
        "location": "vagamon",
        "location_display_name": "Kurisumala Pine Valley, Vagamon",
        "property_type": "bungalow",
        "price_per_night": 32000,
        "bedrooms": 3,
        "bathrooms": 3,
        "max_guests": 6,
        "short_description": "Contemporary rustic mountain bungalow with grey basalt stone walls, charcoal steel frame, heated cedar Jacuzzi deck, and pine valley views.",
        "description": "Perched on a quiet ridge overlooking Vagamon's pine forests and rolling green hill slopes, Pine Ridge Retreat offers rustic luxury redefined. Built with natural grey basalt stone, exposed charcoal steel beams, and floor-to-ceiling glass, it features an outdoor wooden terrace with a steaming heated cedar Jacuzzi and an indoor double-height stone fireplace lounge.",
        "main_image": "/static/images/properties/prop_06/prop_06_img_1.jpg",
        "gallery_json": [
            "/static/images/properties/prop_06/prop_06_img_1.jpg",
            "/static/images/properties/prop_06/prop_06_img_2.jpg",
            "/static/images/properties/prop_06/prop_06_img_3.jpg"
        ],
        "amenities_json": [
            "Heated Outdoor Cedar Jacuzzi", "Basalt Stone Fireplace Lounge", "Pine Forest Valley Views", 
            "Private Mountain Guide", "Barbecue Grill Terrace", "High-speed WiFi", 
            "Custom Highland Dining", "Heated Flooring"
        ],
        "rating": 4.94,
        "reviews_count": 16,
        "is_featured": True
    },
    {
        "title": "Kovalam Horizon Oceanfront Reserve",
        "slug": "kovalam-horizon-oceanfront-reserve",
        "location": "kovalam",
        "location_display_name": "Lighthouse Beach Cove, Kovalam",
        "property_type": "residence",
        "price_per_night": 52000,
        "bedrooms": 5,
        "bathrooms": 6,
        "max_guests": 10,
        "short_description": "Ultra-luxury coastal beach residence with white stucco, teak louvers, multi-tiered cascading infinity pool, and private cove beach access.",
        "description": "Surrounded by swaying coconut palms on a private cliffside overlooking Kovalam's golden sands, Horizon Oceanfront Reserve is Kovalam's premier private residence. Features multi-tiered cascading infinity pools, teak wood louvers, glass oceanfront suites, and private stairway access to a secluded cove beach.",
        "main_image": "/static/images/properties/prop_07/prop_07_img_1.jpg",
        "gallery_json": [
            "/static/images/properties/prop_07/prop_07_img_1.jpg",
            "/static/images/properties/prop_07/prop_07_img_2.jpg",
            "/static/images/properties/prop_07/prop_07_img_3.jpg"
        ],
        "amenities_json": [
            "Multi-Tiered Cascading Infinity Pool", "Private Beach Cove Access", "Ocean View Master Suites", 
            "Full Staff (Butler & Chef)", "Private Elevator Access", "Wellness Spa Suite", 
            "Sonos Outdoor Sound System", "Sub-Zero Gourmet Kitchen"
        ],
        "rating": 4.98,
        "reviews_count": 27,
        "is_featured": True
    },
    {
        "title": "Fort Kochi Maritime Heritage Manor",
        "slug": "fort-kochi-maritime-heritage-manor",
        "location": "fort_kochi",
        "location_display_name": "Heritage Zone, Fort Kochi",
        "property_type": "bungalow",
        "price_per_night": 40000,
        "bedrooms": 4,
        "bathrooms": 4,
        "max_guests": 8,
        "short_description": "Restored Dutch-Portuguese colonial luxury mansion featuring white lime-washed walls, terracotta roofs, and private inner courtyard pool.",
        "description": "Step into rich colonial elegance in the heart of Fort Kochi's art district. This 250-year-old Dutch-Portuguese manor has been meticulously restored into a modern luxury sanctuary, featuring a private turquoise inner courtyard swimming pool, antique teakwood shutters, high timber ceilings, and private chauffeur service for exploring Kochi harbor.",
        "main_image": "/static/images/properties/prop_08/prop_08_img_1.jpg",
        "gallery_json": [
            "/static/images/properties/prop_08/prop_08_img_1.jpg",
            "/static/images/properties/prop_08/prop_08_img_2.jpg",
            "/static/images/properties/prop_08/prop_08_img_3.jpg"
        ],
        "amenities_json": [
            "Private Inner Courtyard Pool", "Restored Dutch-Portuguese Architecture", "Private Vintage Chauffeur", 
            "Antique Art Collection", "Private Wine Cellar & Bar", "Gourmet Kerala Breakfast Included", 
            "High-Speed Fiber WiFi", "24/7 Concierge Service"
        ],
        "rating": 4.97,
        "reviews_count": 42,
        "is_featured": True
    },
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
        "main_image": "/static/images/properties/prop_09/prop_09_img_1.jpg",
        "gallery_json": [
            "/static/images/properties/prop_09/prop_09_img_1.jpg",
            "/static/images/properties/prop_09/prop_09_img_2.jpg",
            "/static/images/properties/prop_09/prop_09_img_3.jpg"
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
        "main_image": "/static/images/properties/prop_10/prop_10_img_1.jpg",
        "gallery_json": [
            "/static/images/properties/prop_10/prop_10_img_1.jpg",
            "/static/images/properties/prop_10/prop_10_img_2.jpg",
            "/static/images/properties/prop_10/prop_10_img_3.jpg"
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
        "main_image": "/static/images/properties/prop_11/prop_11_img_1.jpg",
        "gallery_json": [
            "/static/images/properties/prop_11/prop_11_img_1.jpg",
            "/static/images/properties/prop_11/prop_11_img_2.jpg",
            "/static/images/properties/prop_11/prop_11_img_3.jpg"
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
        "main_image": "/static/images/properties/prop_12/prop_12_img_1.jpg",
        "gallery_json": [
            "/static/images/properties/prop_12/prop_12_img_1.jpg",
            "/static/images/properties/prop_12/prop_12_img_2.jpg",
            "/static/images/properties/prop_12/prop_12_img_3.jpg"
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

class Command(BaseCommand):
    help = 'Seeds initial luxury properties into database and ensures admin superuser'

    def handle(self, *args, **options):
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@rentora.in', 'RentoraAdmin2026!')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin'))
        else:
            u = User.objects.get(username='admin')
            u.set_password('RentoraAdmin2026!')
            u.is_superuser = True
            u.is_staff = True
            u.save()
            self.stdout.write(self.style.SUCCESS('Updated superuser credentials: admin'))

        # Temporary normal user: user / password
        u_temp, created_temp = User.objects.get_or_create(username='user', defaults={'email': 'user@rentora.in'})
        u_temp.set_password('password')
        u_temp.is_staff = False
        u_temp.is_superuser = False
        u_temp.save()
        self.stdout.write(self.style.SUCCESS('Updated normal user credentials: user / password'))


        # Purge legacy properties not in current SAMPLE_PROPERTIES
        valid_slugs = [p['slug'] for p in SAMPLE_PROPERTIES]
        Property.objects.exclude(slug__in=valid_slugs).delete()

        count = 0
        for data in SAMPLE_PROPERTIES:
            obj, created = Property.objects.update_or_create(
                slug=data['slug'],
                defaults=data
            )
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {count} luxury properties (Total in DB: {Property.objects.count()}).'))

