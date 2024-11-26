from rest_framework import serializers
from .utils import *
from .models import *




class AccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = [
                'id', 
                'email', 
                'first_name', 
                'last_name', 
                'profile_picture', 
                'is_email_verified', 
                'gender', 
                'phone_number', 
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
            "password_confirmation": {"write_only": True},
            "age": {"read_only": True},
        }

        def validate(self, data):
            if data["password"] != data["password_confirmation"]:
                raise serializers.ValidationError("Passwords do not match.")
            try:
                validate_password(data["password"])
            except ValidationError as e:
                raise serializers.ValidationError(e.messages)
            return data
        
        def create(self, validated_data):
            validated_data.pop("password_confirmation")
            user = Account.objects.create(**validated_data)
            return user