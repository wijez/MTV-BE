from django.urls import path
from MSRV.apps.user.views import RegisterViewSet, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('register/', RegisterViewSet.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login_api'),
    path('verify/', TokenVerifyView.as_view(), name="token_verify"),
    path('refresh/', TokenRefreshView.as_view(), name="token_refresh"),
]
