from django.urls import path
from .views import CartView, CartItemView, CheckoutView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/item/', CartItemView.as_view(), name='cart_item'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
