from django.urls import path
from MSRV.apps.user.views import UserDetailViewSet

urlpatterns = [
    path('read_me/', UserDetailViewSet.as_view(), name='read_me')
]
