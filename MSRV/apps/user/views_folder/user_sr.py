from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from MSRV.apps.user.models_folder.user_scientific_research import UserScientificResearch
from MSRV.apps.user.serializers_folder.user_sr import UserScientificResearchSerializer


class UserScientificResearchViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserScientificResearch.objects.all()
    serializer_class = UserScientificResearchSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['scientific_research__id',  'user__id']