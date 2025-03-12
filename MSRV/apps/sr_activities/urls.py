from django.urls import path, include

urlpatterns = [
    path('scientific_research_activities/', include('MSRV.apps.sr_activities.routers.scientific_research_activities')),
    path('scientific_research/', include('MSRV.apps.sr_activities.routers.scientific_research'))
]
