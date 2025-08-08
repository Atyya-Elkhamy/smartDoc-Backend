from rest_framework import serializers
import re
from .models import *
class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['username','email','password','phone']

    def validate(self, attrs):
        username = attrs["username"]
        email = attrs["email"]
        password = attrs["password"]
        phone = attrs["phone"]
        username_regex = r'^[a-zA-Z_ ]+$'
        if not re.match(username_regex, username):
            raise serializers.ValidationError({"username": "Only letters, underscores, and spaces are allowed"})
        username = username.strip()
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise serializers.ValidationError({"email":"Invalid email format"})
        password_regex = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
        if not re.match(password_regex, password):
            raise serializers.ValidationError({"password":"Password must be at least 8 characters long and include both letters and numbers"})
        phone_regex = r'^(010|012|015|011)\d{8}$'
        if not re.match(phone_regex, phone):
            raise serializers.ValidationError({"phone":"Phone number must be 11 digits and start with 010, 012, 015, or 011"})
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            phone=validated_data["phone"],
            password=validated_data["password"]
        )
    