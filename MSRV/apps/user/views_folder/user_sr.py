from MSRV.apps.user.views_folder import (
    openapi, viewsets, filters, IsAuthenticated, PermissionDenied, swagger_auto_schema
)

from MSRV.apps.user.models import UserScientificResearch
from MSRV.apps.user.serializers_folder.user_sr import UserScientificResearchSerializer
from MSRV.apps.utils.constant import AppStatus


class UserScientificResearchViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserScientificResearch.objects.all()
    serializer_class = UserScientificResearchSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['scientific_research__id',  'user__id']

    def check_user_in_scientific_research(self):
        user = self.request.user
        scientific_research_id = self.request.query_params.get('scientific_research_id', None)
        return self.queryset.filter(
            scientific_research_id=scientific_research_id,
            user_id=user.id
        ).exists()

    def filter_queryset(self, queryset):
        scientific_research_id = self.request.query_params.get('scientific_research_id', None)

        if not scientific_research_id and not self.request.user.is_superuser:
            raise PermissionDenied(AppStatus.USER_DOES_NOT_PERMIT.message)

        if not self.check_user_in_scientific_research() and not self.request.user.is_superuser:
            raise PermissionDenied(AppStatus.USER_NOT_IN_SCIENTIFIC_RESEARCH.message)

        if scientific_research_id:
            queryset = queryset.filter(scientific_research_id=scientific_research_id)

        return queryset

    @swagger_auto_schema(
        operation_summary="Search Scientific Research ID",
        manual_parameters=[
            openapi.Parameter(
                'scientific_research_id',
                openapi.IN_QUERY,
                description="Scientific Research ID",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)