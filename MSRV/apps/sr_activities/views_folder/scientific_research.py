from MSRV.apps.sr_activities.serializers_folder.scientific_research import UpdateScientificResearchSerializer
from MSRV.apps.sr_activities.views_folder import (
    viewsets, MultiPartParser, FormParser, GenericAPIView, Response
)
from MSRV.apps.sr_activities.models import (
    ScientificResearch
)
from MSRV.apps.sr_activities.serializers import (
    ScientificResearchSerializer,
    CreateScientificResearchSerializer,
    UpdateBannerScientificResearchSerializer
)


class ScientificResearchViewSet(viewsets.ModelViewSet):
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
    queryset = ScientificResearch.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = UpdateBannerScientificResearchSerializer

    def put(self, request, *args, **kwargs):
        scientific_research = self.get_object()
        serializer = self.get_serializer(scientific_research, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(ScientificResearchSerializer(instance).data)
