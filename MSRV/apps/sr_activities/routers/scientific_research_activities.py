from django.urls import path, include
from rest_framework.routers import DefaultRouter
from MSRV.apps.sr_activities.views import ScientificResearchActivitiesViewSet

router = DefaultRouter(trailing_slash=False,)
router.register('', ScientificResearchActivitiesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
