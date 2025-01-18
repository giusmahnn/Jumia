from rest_framework import serializers
from accounts.serializers import AccountSerializer
from accounts.models import *
from products.models import Product
from vendor.models import Vendor



class VendorSerializer(serializers.ModelSerializer):
    user = AccountSerializer()

    class Meta:
        model = Vendor
        fields = [
            'user',
            'store_name',
            'store_description',
            'store_logo',
            'phone_number',
            'nationality',
            'state',
            'city',
            'address',
            ]
        

    def create(self, validated_data):  
        user_data = validated_data.pop('user')  # Extract user data from the validated data  
        
        # Create an AccountSerializer instance to validate and save the user data  
        user_serializer = AccountSerializer(data=user_data)  
        user_serializer.is_valid(raise_exception=True)  # Validate data  
        
        # Save the Account instance with is_seller_user=True  
        user = user_serializer.save(is_seller_user=True)  

        # Now create the Vendor instance with the proper validated data  
        vendor = Vendor.objects.create(user=user, **validated_data)  
        return vendor  


class VendorLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email:
            try:
                user = Account.objects.get(email=email)
            except Account.DoesNotExist:
                raise serializers.ValidationError("Invalid email or password")

            if user.password != password:
                raise serializers.ValidationError("Invalid password")

            data["user"] = user

        return data
    

class VendorProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'vendor',
            'name',
            'slug',
            'category',
            'description',
            'price',
            'discount_price',
            'quantity',
            'image',
            'created_at',
            'updated_at',
        ]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "id": {"read_only": True},
            "vendor": {"read_only": True},
        }


        def create(self, validated_data):
            """
            Creates a new product for the authenticated vendor.

            Parameters:
            validated_data (dict): A dictionary containing the validated data for the product.

            Returns:
            Product: The newly created product instance.

            The function retrieves the authenticated vendor from the request context,
            creates a new product using the provided validated data, and returns the created product instance.
            """
            vendor = self.context['request'].user.vendor
            product = Product.objects.create(vendor=vendor, **validated_data)
            return product