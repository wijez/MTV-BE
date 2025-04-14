import io
import zipfile
from MSRV.apps.sr_activities.serializers_folder import (
    serializers, transaction, AppStatus
)
from MSRV.apps.utils.enum_type import (
    FolderEnum,
    TypeFileEnum,
)

from MSRV.apps.sr_activities.models import ScientificResearch
from MSRV.apps.user.models import User, UserScientificResearch

from MSRV.apps.sr_activities.serializers_folder.scientific_research_activities import ScientificResearchActivitySerializer

from MSRV.apps.utils.api_clone_video import UpLoadFileToClone



class ScientificResearchSerializer(serializers.ModelSerializer):
    sr_activities = ScientificResearchActivitySerializer()

    class Meta:
        model = ScientificResearch
        fields = '__all__'


class CreateScientificResearchSerializer(serializers.ModelSerializer):
    list_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True
    )

    class Meta:
        model = ScientificResearch
        fields = '__all__'
        extra_kwargs = {'banner': {'read_only': True}}

    def create(self, validated_data):
        user = self.context['request'].user
        list_user = validated_data.pop('list_user', [])

        if not user:
            raise serializers.ValidationError(AppStatus.USER_NOT_EXIST.message)

        with transaction.atomic():
            try:
                # Tạo hoạt động khoa học
                scientific_research = super().create(validated_data)

                # Gắn request.user là leader
                UserScientificResearch.objects.create(
                    user=user,
                    scientific_research=scientific_research,
                    is_leader=True
                )

                # Gắn các user khác
                UserScientificResearch.objects.bulk_create([
                    UserScientificResearch(
                        user=u,
                        scientific_research=scientific_research,
                        is_leader=False
                    )
                    for u in list_user if u != user
                ])

                return scientific_research

            except Exception as e:
                print(e)
                raise serializers.ValidationError(AppStatus.REGISTER_SCIENTIFIC_RESEARCH_FAIL.message)


class UpdateScientificResearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScientificResearch
        fields = '__all__'
        extra_kwargs = {'banner': {'read_only': True}}


class UpdateBannerScientificResearchSerializer(serializers.ModelSerializer):
    file_banner = serializers.FileField(allow_empty_file=True, required=False)

    class Meta:
        model = ScientificResearch
        fields = ['file_banner']

    def update(self, instance, validated_data):
        file_banner = validated_data.pop('file_banner', None)
        if file_banner:
            clone = UpLoadFileToClone()
            url = clone.upload_file(file_obj=file_banner, type_file=TypeFileEnum.IMAGE, folder=FolderEnum.BANNER)
            instance.banner = url
            instance.save()
        return instance


class UpdateDataScientificResearchSerializer(serializers.ModelSerializer):
    file_zip = serializers.FileField(allow_empty_file=True, required=False)

    class Meta:
        model = ScientificResearch
        fields = ['file_zip']

    def update(self, instance, validated_data):
        file_zip = validated_data.pop('file_zip', None)
        data_files = []

        if file_zip:
            # Kiểm tra file có đúng định dạng zip không
            if not zipfile.is_zipfile(file_zip):
                raise serializers.ValidationError(AppStatus.FILE_INVALID.message)

            zip_file = zipfile.ZipFile(file_zip)
            clone = UpLoadFileToClone()

            for file_info in zip_file.infolist():
                if file_info.is_dir():
                    continue  # Bỏ qua thư mục

                file_data = zip_file.read(file_info.filename)
                file_obj = io.BytesIO(file_data)
                file_obj.name = file_info.filename  # Đặt tên cho file để upload

                url = clone.upload_file(
                    file_obj=file_obj,
                    type_file=TypeFileEnum.DOCUMENT,
                    folder=FolderEnum.DATA
                )
                data_files.append(url)

            instance.data = data_files
            instance.save()

        return instance
