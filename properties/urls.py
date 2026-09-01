from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_list_view, name='property_list'),
    path('<slug:slug>/', views.property_detail_view, name='property_detail'),
]
