from rest_framework import serializers
from accounts.serializers import AccountSerializer
from accounts.models import *



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