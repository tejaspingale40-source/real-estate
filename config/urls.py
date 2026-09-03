from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from properties import views as prop_views

urlpatterns = [
    # Public Pages
    path('', prop_views.home_view, name='home'),
    path('properties/', include('properties.urls')),
    path('about/', prop_views.about_view, name='about'),
    path('contact/', prop_views.contact_view, name='contact'),
    path('privacy-policy/', prop_views.privacy_policy_view, name='privacy_policy'),
    path('terms-of-service/', prop_views.terms_of_service_view, name='terms_of_service'),

    # Admin
    path('admin/', admin.site.urls),

    # Custom Admin Dashboard Auth & Pages
    path('dashboard/login/', prop_views.dashboard_login_view, name='dashboard_login'),
    path('dashboard/logout/', prop_views.dashboard_logout_view, name='dashboard_logout'),
    path('dashboard/', prop_views.dashboard_view, name='dashboard'),
    path('dashboard/settings/', prop_views.dashboard_site_settings, name='dashboard_site_settings'),
    path('dashboard/properties/', prop_views.dashboard_property_list, name='dashboard_properties'),
    path('dashboard/properties/add/', prop_views.dashboard_property_add, name='dashboard_property_add'),
    path('dashboard/properties/<int:pk>/edit/', prop_views.dashboard_property_edit, name='dashboard_property_edit'),
    path('dashboard/properties/<int:pk>/delete/', prop_views.dashboard_property_delete, name='dashboard_property_delete'),
    path('dashboard/properties/images/<int:pk>/delete/', prop_views.dashboard_property_image_delete, name='dashboard_property_image_delete'),
    path('dashboard/properties/videos/<int:pk>/delete/', prop_views.dashboard_property_video_delete, name='dashboard_property_video_delete'),
    
    # Enquiries Dashboard routes
    path('', include('enquiries.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
