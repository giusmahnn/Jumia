from django.urls import path
from .views import *

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/item/', CartItemView.as_view(), name='cart_item'),
    path('cart/item/<int:pk>/', CartItemDeleteView.as_view(), name='cart_item_delete'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
