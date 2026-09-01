from django.contrib import admin
from .models import Enquiry


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'property', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'phone', 'email', 'message', 'property__title']
    list_editable = ['status']
