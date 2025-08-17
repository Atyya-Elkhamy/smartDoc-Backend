from rest_framework import serializers
import re
from .models import User


class UserSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone', 'address', 'age', 'gender']
        extra_kwargs = {
            "password": {"write_only": True}  
        }
    def validate(self, attrs):
        username = attrs.get("username", "")
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        phone = attrs.get("phone", "")
        address = attrs.get("address", "")
        age = attrs.get("age", 0)
        gender = attrs.get("gender", "")

        if not re.match(r'^[a-zA-Z_ ]+$', username):
            raise serializers.ValidationError({"username": "Only letters, underscores, and spaces are allowed"})
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise serializers.ValidationError({"email": "Invalid email format"})
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long and include both letters and numbers"})
        if not re.match(r'^(010|012|015|011)\d{8}$', phone):
            raise serializers.ValidationError({"phone": "Phone number must be 11 digits and start with 010, 012, 015, or 011"})
        if not isinstance(address, str) or not address.strip():
            raise serializers.ValidationError({"address": "Address is required"})
        if not isinstance(age, int) or age <= 0:
            raise serializers.ValidationError({"age": "Age must be a positive integer"})
        if gender not in ["male", "female"]:
            raise serializers.ValidationError({"gender": "Gender must be 'male' or 'female'"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            phone=validated_data["phone"],
            password=validated_data["password"]
        )
        user.address = validated_data.get("address")
        user.age = validated_data.get("age")
        user.gender = validated_data.get("gender")
        user.save()
        return user
