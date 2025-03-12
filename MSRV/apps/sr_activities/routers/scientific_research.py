from django.urls import path, include
from rest_framework.routers import DefaultRouter
from MSRV.apps.sr_activities.views import ScientificResearchViewSet

router = DefaultRouter(trailing_slash=False,)
router.register('', ScientificResearchViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
