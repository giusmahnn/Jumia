from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    # on_sale = serializers.SerializerMethodField()
    # discount_percentage = serializers.SerializerMethodField()
    store_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'store_name',
            'name',
            'slug',
            'category',
            'description',
            'price',
            # 'discount_price',
            # 'discount_percentage',
            # 'on_sale',
            'quantity',
            'image',
            'created_at',
            'updated_at',
        ]
        extra_kwargs = {
            'vendor': {'read_only': True},
            # 'on_sale': {'read_only': True},
            # 'discount_percentage': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'id': {'read_only': True},
            'slug': {'read_only': True},

        }
    
    def get_store_name(slef, obj):
        return obj.vendor.store_name

    # def is_on_sale(self, obj):
    #     return obj.is_on_sale
    
    # def discount_percentage(self, obj):
    #     return obj.discount_percentage