from django.urls import path
from MSRV.apps.user.views import UserDetailViewSet, UpdateUserViewSet

urlpatterns = [
    path('read_me/', UserDetailViewSet.as_view(), name='read_me'),
    path('update_me/', UpdateUserViewSet.as_view(), name='update_me')
]
