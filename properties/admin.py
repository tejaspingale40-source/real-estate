from django.contrib import admin
from .models import Property, PropertyImage, PropertyVideo, Amenity, SiteSettings

# Customize Django Native Admin Panel Branding
admin.site.site_header = "PERFECT HOMES Administration"
admin.site.site_title = "PERFECT HOMES Admin Portal"
admin.site.index_title = "Welcome to PERFECT HOMES Control Panel"


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


class PropertyVideoInline(admin.TabularInline):
    model = PropertyVideo
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'location', 'property_type', 'purpose', 'status', 'featured', 'created_at']
    list_filter = ['property_type', 'purpose', 'status', 'featured', 'location']
    search_fields = ['title', 'location', 'address', 'description']
    list_editable = ['status', 'featured', 'price']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('amenities',)
    inlines = [PropertyImageInline, PropertyVideoInline]


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    search_fields = ['name']


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'image', 'is_cover', 'order']
    list_filter = ['is_cover']
    search_fields = ['property__title']


@admin.register(PropertyVideo)
class PropertyVideoAdmin(admin.ModelAdmin):
    list_display = ['property', 'title', 'video', 'created_at']
    search_fields = ['property__title', 'title']


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'phone', 'email', 'about_founder_name']
    fieldsets = (
        ('General Brand & Contact Settings', {
            'fields': ('site_name', 'tagline', 'phone', 'email', 'address')
        }),
        ('About Page Content', {
            'fields': ('about_subtitle', 'about_vision_heading', 'about_vision_text', 'about_quote', 'about_founder_name')
        }),
        ('Contact Page Content', {
            'fields': ('contact_subtitle', 'contact_address', 'contact_hours', 'google_maps_url')
        }),
    )

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
