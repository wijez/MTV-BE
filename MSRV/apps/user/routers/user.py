from django.urls import path, include
from rest_framework.routers import DefaultRouter
from MSRV.apps.user.views import (
    UserDetailViewSet,
    UpdateUserViewSet,
    AdminUserViewSet,
    ImportUsersFromCSV,
    UserSearchView,
)


router = DefaultRouter(trailing_slash=False,)
router.register('', AdminUserViewSet )

urlpatterns = [
    path('read_me/', UserDetailViewSet.as_view(), name='read_me'),
    path('update_me/', UpdateUserViewSet.as_view(), name='update_me'),
    path('', include(router.urls)),
    path("admin/import-users/", ImportUsersFromCSV.as_view(), name="import-users"),
    path('search/', UserSearchView.as_view(), name="search user"),
]
