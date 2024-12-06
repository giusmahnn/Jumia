from rest_framework import serializers
from .models import *





class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            'id',
            'cart',
            'product',
            'quantity',
            'price',
            'get_total_price',
        ]
        extra_kwargs = {
            'get_total_price': {'read_only': True},
            'id': {'read_only': True},
        }



class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'cart_items',
            'created_at',
            'get_total_price',
            'get_summary',
            'get_full_address',
            'get_address_as_string',
        ]
        extra_kwargs = {
            'get_total_price': {'read_only': True},
            'get_summary': {'read_only': True},
            'get_full_address': {'read_only': True},
            'get_address_as_string': {'read_only': True},
            'id': {'read_only': True},
            'user': {'read_only': True},
            'cart_items': {'read_only': True},
            'created_at': {'read_only': True},
        }

        def get_total_price(self, obj):
            return sum(item.get_total_price() for item in obj.cart_items.all())
        
        def get_summary(self, obj):
            return f"{obj.user.email}'s Cart ({len(obj.cart_items.all())} items)"

















class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        models = OrderItem
        fields = '__all__'



class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemsSerializer(many=True)
    shipping_address = ShippingAddressSerializer()

    class Meta:
        model = Order
        fields = '__all__'
        



    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        shipping_address_data = validated_data.pop('shipping_address')

        order = Order.objects.create(**validated_data)

        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)

        shipping_address = ShippingAddress.objects.create(order=order, **shipping_address_data)

        return order
    
    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('order_items', None)
        shipping_address_data = validated_data.pop('shipping_address', None)

        instance.update(**validated_data)

        if order_items_data:
            for item_data in order_items_data:
                OrderItem.objects.update_or_create(order=instance, **item_data)

        if shipping_address_data:
            shipping_address, _ = ShippingAddress.objects.update_or_create(order=instance, **shipping_address_data)

        return instance