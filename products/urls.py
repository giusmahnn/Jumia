from django.urls import path
from .views import *


urlpatterns = [
    path("product/", ProductView.as_view()),
    path("product/search/", ProductSearchView.as_view()),
    path("products/<int:pk>/", ProductDetailView.as_view())
]