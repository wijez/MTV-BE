from MSRV.apps.sr_activities.views_folder import (
    viewsets
)
from MSRV.apps.sr_activities.models import (
    ScientificResearchActivity
)
from MSRV.apps.sr_activities.serializers import (
    ScientificResearchActivitySerializer
)


class ScientificResearchActivitiesViewSet(viewsets.ModelViewSet):
    queryset = ScientificResearchActivity.objects.all()
    serializer_class = ScientificResearchActivitySerializer
