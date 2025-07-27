from django.urls import path
from .views import * 

urlpatterns = [
    path("search/", ProductSearchAPIView.as_view(), name="search_view"),
]
