from django.urls import path
from .views import *



urlpatterns = [
    path("vendor-signup/", VendorCreateView.as_view()),
    path("vendor-login/", VendorLoginView.as_view()),
    path("vendor-products/", CreateProduct.as_view()),
    path('vendor-dashboard/', VendorDashboardView.as_view(), name='vendor-dashboard'),
    path('delete-products/', Delete.as_view(), name='delete-products'),  # Add this line to your URL patterns.
]