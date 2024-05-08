from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import data_signup, data_search, data_login

urlpatterns = [
    path('signup/', data_signup),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('login/', data_login),
    path('search/', data_search),
]
