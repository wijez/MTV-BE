from rest_framework import serializers
from MSRV.apps.user.models_folder.user_scientific_research import UserScientificResearch
from MSRV.apps.sr_activities.models_folder.scientific_research import ScientificResearch
from MSRV.apps.user.models import User

class UserScientificResearchSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    scientific_research = serializers.PrimaryKeyRelatedField(queryset=ScientificResearch.objects.all())

    class Meta:
        model = UserScientificResearch
        fields = ['id', 'user', 'scientific_research', 'point', 'is_leader', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
