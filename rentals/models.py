import uuid
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

LOCATION_CHOICES = [
    ('alleppey', 'Alleppey (Alappuzha) - Backwaters'),
    ('munnar', 'Munnar - Tea Estates & Misty Hills'),
    ('varkala', 'Varkala - Cliffside Oceanfront'),
    ('fort_kochi', 'Fort Kochi - Heritage & Culture'),
    ('wayanad', 'Wayanad - Rainforest & Sanctuary'),
    ('kumarakom', 'Kumarakom - Lake & Lagoon'),
    ('vagamon', 'Vagamon - Misty Pine Valleys'),
    ('kovalam', 'Kovalam - Gold Sand Coastal Reserve'),
    ('athirappilly', 'Athirappilly - Rainforest & Waterfalls'),
    ('thekkady', 'Thekkady - Spice Plantation Sanctuary'),
    ('idukki', 'Idukki - High Range Valleys'),
    ('kannur', 'Kannur - Malabar Coast Cliffs'),
]

PROPERTY_TYPE_CHOICES = [
    ('villa', 'Luxury Private Villa'),
    ('houseboat', 'Heritage Houseboat'),
    ('estate', 'Plantation Estate Manor'),
    ('bungalow', 'Colonial Heritage Bungalow'),
    ('cottage', 'Cliffside Ocean Cottage'),
    ('residence', 'Modern High-End Residence'),
]

class Property(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=220)
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    location_display_name = models.CharField(max_length=100, default='Kerala')
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField(default=2)
    bathrooms = models.PositiveIntegerField(default=2)
    max_guests = models.PositiveIntegerField(default=4)
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    main_image = models.URLField(max_length=500)
    gallery_json = models.JSONField(default=list, blank=True)
    amenities_json = models.JSONField(default=list, blank=True)
    rating = models.FloatField(default=4.9)
    reviews_count = models.PositiveIntegerField(default=18)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['-is_featured', '-rating']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Inquiry(models.Model):
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, related_name='inquiries')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    guests = models.PositiveIntegerField(default=2)
    message = models.TextField()
    status = models.CharField(max_length=20, default='Pending', choices=[('Pending', 'Pending'), ('Contacted', 'Contacted'), ('Confirmed', 'Confirmed')])
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Inquiries"
        ordering = ['-created_at']

    def __str__(self):
        prop_title = self.property.title if self.property else "General Inquiry"
        return f"Inquiry from {self.name} for {prop_title}"

class VisitorLog(models.Model):
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    page_url = models.CharField(max_length=300)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, related_name='visitor_logs')
    user_agent = models.TextField(blank=True, default='')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Visitor & Click Logs"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.ip_address} visited {self.page_url} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

def generate_token_str():
    return str(uuid.uuid4())

class EmailVerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_verification_token')
    token = models.CharField(max_length=64, unique=True, default=generate_token_str)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Email Verification Tokens"

    def __str__(self):
        return f"Token for {self.user.username} ({'Verified' if self.is_verified else 'Pending'})"
