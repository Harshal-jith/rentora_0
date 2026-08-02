from django.core.management.base import BaseCommand
from rentals.models import Property

SAMPLE_PROPERTIES = [
    {
        "title": "The Sovereign Alleppey Backwater Villa",
        "slug": "sovereign-alleppey-backwater-villa",
        "location": "alleppey",
        "location_display_name": "Punnamada Backwaters, Alleppey",
        "property_type": "villa",
        "price_per_night": 35000,
        "bedrooms": 4,
        "bathrooms": 4,
        "max_guests": 8,
        "short_description": "Exclusive private waterfront sanctuary with direct backwater access, private infinity pool, and dedicated butler service.",
        "description": "Nestled on the serene banks of Lake Vembanad in Alleppey, The Sovereign Villa offers an extraordinary blend of traditional Kerala architecture and modern luxury. Featuring handcrafted teakwood interiors, floor-to-ceiling glass walls overlooking emerald coconut groves, a private infinity pool that merges seamlessly with the backwaters, and a private dock equipped with a luxury sunset cruiser.",
        "main_image": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=1200&q=80",
        "gallery_json": [
            "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1571896349842-33c89424de2d?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&w=1200&q=80"
        ],
        "amenities_json": [
            "Private Infinity Pool", "Direct Backwater Deck", "Private Chef & Butler", 
            "Sunset Kayaks", "Heated Jacuzzi", "High-speed Starlink WiFi", 
            "Ayurvedic Spa Lounge", "Air Conditioning", "Helipad Transfer Available"
        ],
        "rating": 4.98,
        "reviews_count": 32,
        "is_featured": True
    },
    {
        "title": "Munnar Tea Country Heritage Manor",
        "slug": "munnar-tea-country-heritage-manor",
        "location": "munnar",
        "location_display_name": "Old Munnar Hills, Munnar",
        "property_type": "estate",
        "price_per_night": 48000,
        "bedrooms": 5,
        "bathrooms": 5,
        "max_guests": 10,
        "short_description": "Restored 1920s British colonial tea plantation manor perched high amidst misty peaks and rolling tea gardens.",
        "description": "Perched 1,600 meters above sea level, Munnar Tea Country Manor is a palatial heritage estate surrounded by 150 acres of private organic tea plantations. Enjoy crisp mountain breezes from your wraparound veranda, cozy up by stone fireplaces in every suite, and savour custom farm-to-table cuisine prepared by top culinary masters.",
        "main_image": "https://images.unsplash.com/photo-1596178065887-1198b6148b2b?auto=format&fit=crop&w=1200&q=80",
        "gallery_json": [
            "https://images.unsplash.com/photo-1596178065887-1198b6148b2b?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
        ],
        "amenities_json": [
            "150-Acre Private Plantation", "Stone Fireplaces in Suites", "Farm-to-Table Dining", 
            "Guided Tea Tasting Tours", "Heated Plunge Pool", "High-speed WiFi", 
            "Personal Sommelier", "Mountain View Terraces"
        ],
        "rating": 4.95,
        "reviews_count": 28,
        "is_featured": True
    },
    {
        "title": "Varkala Cliffside Azure Ocean Villa",
        "slug": "varkala-cliffside-azure-ocean-villa",
        "location": "varkala",
        "location_display_name": "North Cliff Promenade, Varkala",
        "property_type": "cottage",
        "price_per_night": 28000,
        "bedrooms": 3,
        "bathrooms": 3,
        "max_guests": 6,
        "short_description": "Panoramas of the Arabian Sea from your private cliffside sanctuary with private beach access and open-air therapy baths.",
        "description": "Architectural masterpiece perched right on Varkala's famous red laterite cliffs. Features dramatic floor-to-ceiling ocean views, open-air rainforest showers, a private yoga deck suspended over the waves, and a dedicated team of wellness therapists and private chefs.",
        "main_image": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80",
        "gallery_json": [
            "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80"
        ],
        "amenities_json": [
            "Unobstructed Ocean View", "Private Beach Access Staircase", "Cliffside Yoga Deck", 
            "Open-Air Rain Shower", "Ayurvedic Doctor Consultation", "Seafood Grill Master", 
            "Infinity Edge Plunge Pool", "Sonos Sound System"
        ],
        "rating": 4.92,
        "reviews_count": 19,
        "is_featured": True
    },
    {
        "title": "The Malabar Colonial Grand Bungalow",
        "slug": "the-malabar-colonial-grand-bungalow",
        "location": "fort_kochi",
        "location_display_name": "Heritage Zone, Fort Kochi",
        "property_type": "bungalow",
        "price_per_night": 42000,
        "bedrooms": 4,
        "bathrooms": 4,
        "max_guests": 8,
        "short_description": "A 300-year-old Dutch-Portuguese colonial luxury mansion with private courtyard pool and antique art collection.",
        "description": "Step into history in the heart of Fort Kochi. Meticulously restored with Dutch tiles, antique rosewood furniture, private courtyard swimming pool, and an air-conditioned private library. Includes private chauffeur service for exploring Fort Kochi's art galleries, spice markets, and Chinese fishing nets.",
        "main_image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80",
        "gallery_json": [
            "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=1200&q=80"
        ],
        "amenities_json": [
            "Courtyard Swimming Pool", "Private Vintage Chauffeur", "Antique Art Collection", 
            "Private Library & Bar", "Gourmet Breakfast Included", "Concierge Service", 
            "High-Speed Fiber WiFi"
        ],
        "rating": 4.97,
        "reviews_count": 45,
        "is_featured": False
    },
    {
        "title": "Wayanad Canopy Glass Eco Sanctuary",
        "slug": "wayanad-canopy-glass-eco-sanctuary",
        "location": "wayanad",
        "location_display_name": "Lakkidi Rainforest, Wayanad",
        "property_type": "villa",
        "price_per_night": 32000,
        "bedrooms": 3,
        "bathrooms": 3,
        "max_guests": 6,
        "short_description": "Ultra-modern glass structure suspended in the Western Ghats rainforest canopy with private stream pool.",
        "description": "Immerse yourself in untouched wilderness without compromising on world-class luxury. Glass walls wrap around plush king suites suspended 40 feet above the forest floor. Listen to exotic birds and rainforest streams from your heated Jacuzzi.",
        "main_image": "https://images.unsplash.com/photo-1510798831971-661eb04b3739?auto=format&fit=crop&w=1200&q=80",
        "gallery_json": [
            "https://images.unsplash.com/photo-1510798831971-661eb04b3739?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=1200&q=80"
        ],
        "amenities_json": [
            "Rainforest Canopy Suspension", "Private Stream Bathing Pool", "Glass Observatory Room", 
            "Heated Outdoor Jacuzzi", "Private Naturalist Guide", "Organic Plantation Meals"
        ],
        "rating": 4.96,
        "reviews_count": 22,
        "is_featured": True
    },
    {
        "title": "Vembanad Presidential Floating Palace",
        "slug": "vembanad-presidential-floating-palace",
        "location": "kumarakom",
        "location_display_name": "Vembanad Lake, Kumarakom",
        "property_type": "houseboat",
        "price_per_night": 55000,
        "bedrooms": 3,
        "bathrooms": 3,
        "max_guests": 6,
        "short_description": "Ultra-luxury 3-bedroom Kettuvallam houseboat featuring air-conditioned glass lounge and upper sun deck.",
        "description": "The pinnacle of backwater luxury. This handcrafted 120-foot houseboat features three spacious glass-fronted bedrooms, a private chef specializing in Karimeen Pollichathu and fresh backwater seafood, an upper-deck lounge with plush sunbeds, and a private motorboat tender for narrow canal explorations.",
        "main_image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=80",
        "gallery_json": [
            "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=1200&q=80"
        ],
        "amenities_json": [
            "24/7 Air-Conditioned Suites", "Upper Sun Deck & Cocktail Bar", "Full Time Master Captain & Chef", 
            "Private Speedboat Tender", "Live Sitar Performance Onboard", "Unlimited Cruise Routing"
        ],
        "rating": 5.0,
        "reviews_count": 16,
        "is_featured": True
    },
    {
        "title": "Kovalam Royal Palms Ocean Estate",
        "slug": "kovalam-royal-palms-ocean-estate",
        "location": "kovalam",
        "location_display_name": "Private Cove, Kovalam Beach",
        "property_type": "estate",
        "price_per_night": 52000,
        "bedrooms": 5,
        "bathrooms": 6,
        "max_guests": 10,
        "short_description": "Private beachside sanctuary surrounded by towering coconut palms with private sandy cove & infinity pool.",
        "description": "Located on an exclusive private promontory in Kovalam, the Royal Palms Ocean Estate offers direct access to a private secluded beach cove. Features an Olympic-length infinity pool overlooking the Arabian Sea, private open-air dining pavilions, and dedicated Ayurvedic massage therapists.",
        "main_image": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?auto=format&fit=crop&w=1200&q=80",
        "gallery_json": [
            "https://images.unsplash.com/photo-1571896349842-33c89424de2d?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=1200&q=80"
        ],
        "amenities_json": [
            "Private Sandy Beach Cove", "Olympic Infinity Pool", "Personal Ayurvedic Therapists", 
            "Seafood Culinary Master", "Helipad & Yacht Docking", "24/7 Butler Service"
        ],
        "rating": 4.99,
        "reviews_count": 21,
        "is_featured": True
    },
    {
        "title": "Athirappilly Forest Mist Waterfall Chalet",
        "slug": "athirappilly-forest-mist-waterfall-chalet",
        "location": "athirappilly",
        "location_display_name": "Vazhachal Forest Reserve, Athirappilly",
        "property_type": "chalet",
        "price_per_night": 36000,
        "bedrooms": 3,
        "bathrooms": 3,
        "max_guests": 6,
        "short_description": "Modern teakwood chalet perched over river cascades and mist-clad forest waterfalls with private heated hot tub.",
        "description": "Experience the majestic sound of cascading waterfalls from your private glass lounge. Nestled inside the dense Vazhachal forest reserve, this eco-luxury chalet features local teakwood craftsmanship, private riverfront observation deck, heated outdoor hot tub, and private jungle safari tours.",
        "main_image": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1200&q=80",
        "gallery_json": [
            "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1510798831971-661eb04b3739?auto=format&fit=crop&w=1200&q=80"
        ],
        "amenities_json": [
            "Waterfall Panorama Deck", "Private Riverfront Lounge", "Heated Forest Hot Tub", 
            "Guided Jungle Safaris", "Organic Wild Honey Tastings", "24/7 Concierge"
        ],
        "rating": 4.94,
        "reviews_count": 17,
        "is_featured": False
    },
    {
        "title": "Bekal Fort Sunset Sands Villa",
        "slug": "bekal-fort-sunset-sands-villa",
        "location": "kasaragod",
        "location_display_name": "Bekal Fort Promenade, Kasaragod",
        "property_type": "villa",
        "price_per_night": 44000,
        "bedrooms": 4,
        "bathrooms": 4,
        "max_guests": 8,
        "short_description": "Beachfront villa steps away from historic Bekal Fort with private illuminated infinity plunge pool.",
        "description": "Combining northern Kerala coastal heritage with modern resort luxury. Enjoy front-row views of Bekal Fort illuminated at dusk, relax in your private heated infinity plunge pool, and indulge in authentic Malabar seafood dining curated by master chefs.",
        "main_image": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=1200&q=80",
        "gallery_json": [
            "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1571896349842-33c89424de2d?auto=format&fit=crop&w=1200&q=80"
        ],
        "amenities_json": [
            "Bekal Fort Sunset View", "Illuminated Infinity Plunge Pool", "Authentic Malabar Seafood Chef", 
            "Private Beach Access", "Ayurvedic Wellness Spa", "High-Speed WiFi"
        ],
        "rating": 4.97,
        "reviews_count": 25,
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

        # Seed or update temporary demo user: user / password
        if not User.objects.filter(username='user').exists():
            User.objects.create_user(username='user', email='user@rentora.in', password='password')
            self.stdout.write(self.style.SUCCESS('Created demo user: user/password'))
        else:
            u = User.objects.get(username='user')
            u.set_password('password')
            u.save()
            self.stdout.write(self.style.SUCCESS('Updated demo user credentials: user/password'))

        count = 0
        for data in SAMPLE_PROPERTIES:
            obj, created = Property.objects.update_or_create(
                slug=data['slug'],
                defaults=data
            )
            if created:
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {count} new properties (Total in database: {Property.objects.count()}).'))
