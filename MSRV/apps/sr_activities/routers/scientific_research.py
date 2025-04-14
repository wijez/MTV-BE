from django.urls import path, include
from rest_framework.routers import DefaultRouter
from MSRV.apps.sr_activities.views import ScientificResearchViewSet
from MSRV.apps.sr_activities.views_folder.scientific_research import (
    UpdateDataScientificResearchViewSet,
    UpdateBannerScientificResearchViewSet,
)

router = DefaultRouter(trailing_slash=False,)
router.register('', ScientificResearchViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<uuid:pk>/update_banner', UpdateBannerScientificResearchViewSet.as_view()),
    path('<uuid:pk>/update_data', UpdateDataScientificResearchViewSet.as_view()),
]
