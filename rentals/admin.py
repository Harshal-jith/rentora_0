from django.contrib import admin
from .models import Property, Inquiry

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'property_type', 'price_per_night', 'rating', 'is_featured')
    list_filter = ('location', 'property_type', 'is_featured')
    search_fields = ('title', 'description', 'location_display_name')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'property', 'check_in', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
