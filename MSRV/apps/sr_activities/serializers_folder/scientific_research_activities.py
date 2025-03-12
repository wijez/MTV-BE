from MSRV.apps.sr_activities.serializers_folder import (
    serializers
)
from MSRV.apps.sr_activities.models import (
    ScientificResearchActivity
)

class ScientificResearchActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScientificResearchActivity
        fields = '__all__'
