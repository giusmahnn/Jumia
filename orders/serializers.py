from rest_framework import serializers
from .models import *


class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
                'id', 
                'product', 
                'quantity', 
                'total_price'
            ]

    def get_total_price(self, obj):
        return obj.get_total_price()




class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
                'id', 
                'user', 
                'cart_items', 
                'total_price'
            ]

    def get_total_price(self, obj):
        return sum(item.get_total_price() for item in obj.cart_items.all())


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id', 
            'product', 
            'quantity', 
            'price'
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = ShippingAddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 
            'vendor', 
            'customer', 
            'items', 
            'status', 
            'order_date', 
            'shipping_address'
        ]
