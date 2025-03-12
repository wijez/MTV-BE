from MSRV.apps.user.models_folder.user_profile import UserProfile
from MSRV.apps.user.serializers_folder import (
    serializers
)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['user']
