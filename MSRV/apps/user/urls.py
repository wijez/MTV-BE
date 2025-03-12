from django.urls import path, include

urlpatterns = [
    path('user/', include('MSRV.apps.user.routers.user')),
    path('auth/', include('MSRV.apps.user.routers.auth')),
]