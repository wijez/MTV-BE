from MSRV.apps.sr_activities.models import (
    ScientificResearch
)
from MSRV.apps.sr_activities.serializers import (
    ScientificResearchSerializer,
    CreateScientificResearchSerializer,
    UpdateBannerScientificResearchSerializer
)
from MSRV.apps.sr_activities.serializers_folder.scientific_research import (
    UpdateScientificResearchSerializer,
    UpdateDataScientificResearchSerializer
)
from MSRV.apps.sr_activities.views_folder import (
    viewsets, MultiPartParser, FormParser, GenericAPIView, Response, IsAuthenticated, PermissionDenied, AppStatus
)
from MSRV.apps.user.models import (
    UserScientificResearch
)


def check_user_is_leader_scientific_research(user, scientific_research):
    return UserScientificResearch.objects.filter(
        is_leader=True,
        user=user,
        scientific_research=scientific_research
    ).exists()


class ScientificResearchViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ScientificResearch.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ScientificResearchSerializer
        elif self.request.method == 'POST':
            return CreateScientificResearchSerializer
        elif self.request.method == 'PUT':
            return UpdateScientificResearchSerializer
        return ScientificResearchSerializer


class UpdateBannerScientificResearchViewSet(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = ScientificResearch.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = UpdateBannerScientificResearchSerializer

    def put(self, request, *args, **kwargs):
        scientific_research = self.get_object()

        if not check_user_is_leader_scientific_research(user=request.user, scientific_research=scientific_research):
            raise PermissionDenied(AppStatus.SCIENTIFIC_RESEARCH_PERMISSION_DENIED.message)

        serializer = self.get_serializer(scientific_research, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(ScientificResearchSerializer(instance).data)


class UpdateDataScientificResearchViewSet(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = ScientificResearch.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = UpdateDataScientificResearchSerializer

    def put(self, request, *args, **kwargs):
        scientific_research = self.get_object()

        if not check_user_is_leader_scientific_research(user=request.user, scientific_research=scientific_research):
            raise PermissionDenied(AppStatus.SCIENTIFIC_RESEARCH_PERMISSION_DENIED.message)

        serializer = self.get_serializer(scientific_research, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(ScientificResearchSerializer(instance).data)
