from MSRV.apps.sr_activities.views_folder import (
    viewsets, IsAuthenticated
)
from MSRV.apps.sr_activities.models import (
    ScientificResearchActivity
)
from MSRV.apps.sr_activities.serializers import (
    ScientificResearchActivitySerializer
)


class ScientificResearchActivitiesViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ScientificResearchActivity.objects.all()
    serializer_class = ScientificResearchActivitySerializer
