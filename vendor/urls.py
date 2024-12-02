from django.urls import path
from .views import *



urlpatterns = [
    path("vendor-signup/", VendorCreateView.as_view()),
    path("vendor-login/", VendorLoginView.as_view()),
]