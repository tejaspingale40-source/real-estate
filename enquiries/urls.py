from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/enquiries/', views.dashboard_enquiries_list, name='dashboard_enquiries'),
    path('dashboard/enquiries/<int:pk>/status/', views.dashboard_enquiry_update_status, name='dashboard_enquiry_update_status'),
    path('enquiry/quick-submit/', views.quick_enquiry_submit, name='quick_enquiry_submit'),
]
