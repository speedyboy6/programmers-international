from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    # Add URL patterns here later
    # Example: path('', views.product_list, name='product_list'),
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    # Add URL for enquiry submission later
    # PDF export is handled via admin action now.
]