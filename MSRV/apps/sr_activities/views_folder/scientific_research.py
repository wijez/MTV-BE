from MSRV.apps.sr_activities.views_folder import (
    viewsets
)
from MSRV.apps.sr_activities.models import (
    ScientificResearch
)
from MSRV.apps.sr_activities.serializers import (
    ScientificResearchSerializer,
    CreateScientificResearchSerializer
)


class ScientificResearchViewSet(viewsets.ModelViewSet):
    queryset = ScientificResearch.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ScientificResearchSerializer
        return CreateScientificResearchSerializer
