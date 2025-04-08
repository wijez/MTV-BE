from rest_framework.routers import DefaultRouter
from django.urls import path, include
from MSRV.apps.user.views_folder.user_sr import UserScientificResearchViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'user_sr', UserScientificResearchViewSet, basename='user-scientific-research')

urlpatterns = [
    path('', include(router.urls)),
]