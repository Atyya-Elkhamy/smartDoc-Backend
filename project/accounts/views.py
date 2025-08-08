from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from .models import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

# login serializer and view 
# --------------------------------------------------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
     def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({"username": "No user with this username."})
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError({"password": "Incorrect password."})
        data = super().validate(attrs)
        data["user"] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        return data
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
# -------------------------------------------------------------------

class CreateUserView(APIView):
    def get(self, request):
        users = User.objects.all()
        if not users.exists():
            return Response({"response": "No users found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

