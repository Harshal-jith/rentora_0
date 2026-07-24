from django.contrib import admin
from .models import Property, Inquiry, VisitorLog

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'property_type', 'price_per_night', 'rating', 'is_featured')
    list_filter = ('location', 'property_type', 'is_featured')
    search_fields = ('title', 'description', 'location_display_name')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'property', 'ip_address', 'check_in', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'phone', 'ip_address', 'message')

@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'page_url', 'property', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('ip_address', 'page_url', 'user_agent')
    readonly_fields = ('ip_address', 'page_url', 'property', 'user_agent', 'timestamp')
