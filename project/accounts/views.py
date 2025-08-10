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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'] = serializers.EmailField()
        self.fields.pop(self.username_field)  # remove "username"

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "No user with this email."})

        user = authenticate(username=user.username, password=password)
        if user is None:
            raise serializers.ValidationError({"password": "Incorrect password."})

        data = super().validate({"username": user.username, "password": password})
        data["token"] = data.pop("access")
        data["user"] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.type,
        }
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["role"] = user.type
        return token


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

class PatientListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        patients = User.objects.filter(type=User.UserType.PATIENT)
        serializer = UserSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)