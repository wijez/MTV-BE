from django.urls import path, include

urlpatterns = [
    path('sponsorship_proposal/', include('MSRV.apps.sponsorship_proposal.routers.sponsorship_proposal')),
]
