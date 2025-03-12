from MSRV.apps.sr_activities.serializers_folder import (
    serializers
)
from MSRV.apps.sr_activities.models import (
    ScientificResearch
)
from MSRV.apps.sr_activities.serializers_folder.scientific_research_activities import ScientificResearchActivitySerializer

class ScientificResearchSerializer(serializers.ModelSerializer):
    sr_activities = ScientificResearchActivitySerializer()

    class Meta:
        model = ScientificResearch
        fields = '__all__'

class CreateScientificResearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScientificResearch
        fields = '__all__'
