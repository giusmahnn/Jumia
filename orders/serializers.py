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
    total_price = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = [ 
            'product',
            'quantity', 
            'price',
            'total_price'
        ]
    def get_total_price(self, obj):
        return obj.get_total_price()
    def get_product(self, obj):
        return obj.product.name
    


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = ShippingAddressSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 
            'vendor', 
            'customer', 
            'items', 
            'status', 
            'order_date',
            'total_price',
            'shipping_address'
        ]

    def get_total_price(self, obj):
        return obj.calculate_total_price()