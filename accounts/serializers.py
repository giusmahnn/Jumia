from rest_framework import serializers
from .utils import *
from .models import *




class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password_confirmation = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Account
        fields = [
                'id', 
                'email', 
                'first_name', 
                'last_name', 
                'profile_picture', 
                'is_email_verified',
                'date_of_birth', 
                'age', 
                'gender', 
                'phone_number',
                'password',
                'password_confirmation'
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


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField()


class ResetPasswordSerializer(serializers.Serializer):
    otp = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        if not validate_otp(data["otp"]):
            raise serializers.ValidationError("Invalid OTP.")
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        try:
            validate_password(data["password"])
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return data



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
                'profile_picture',
                'email', 
                'first_name', 
                'last_name',
                'gender', 
                'phone_number',
                'date_of_birth',
                'age',
        ]
        extra_kwargs = {
            "age": {"read_only": True},
        }