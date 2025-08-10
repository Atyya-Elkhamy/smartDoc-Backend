from django.urls import path
from .views import * 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="login_view"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh_view"),
    path("create/", CreateUserView.as_view(), name="create_user"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("all-patients/",PatientListView.as_view(),name="list patients"),
]
