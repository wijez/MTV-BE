from MSRV.apps.user.models_folder.user_profile import UserProfile
from MSRV.apps.utils.api_clone_video import UpLoadFileToClone
from MSRV.apps.user.serializers_folder import (
    serializers
)
from MSRV.apps.utils.enum_type import (
    FolderEnum,
    TypeFileEnum,
)


class UserProfileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(allow_empty_file=True, required=False)

    class Meta:
        model = UserProfile
        exclude = ['user']
        extra_kwargs = {'avatar': {'read_only': True},
                        'base_point': {'read_only': True},
                        'created_at': {'read_only': True},
                        'updated_at': {'read_only': True}
                        }

    def update(self, instance, validated_data):
        file = validated_data.pop('file', None)
        if file:
            clone = UpLoadFileToClone()
            url = clone.upload_file(file_obj=file, type_file=TypeFileEnum.IMAGE, folder=FolderEnum.AVATAR)
            instance.avatar = url

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
