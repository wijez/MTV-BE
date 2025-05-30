import io
import zipfile
import mimetypes
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


class UserPointSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    point = serializers.FloatField(min_value=0, required=False)


class CreateScientificResearchSerializer(serializers.ModelSerializer):
    list_user = UserPointSerializer(many=True, write_only=True)

    class Meta:
        model = ScientificResearch
        fields = '__all__'
        extra_kwargs = {'banner': {'read_only': True}}

    def create(self, validated_data):
        user = self.context['request'].user
        list_user_data = validated_data.pop('list_user', [])

        if not user:
            raise serializers.ValidationError(AppStatus.USER_NOT_EXIST.message)

        with transaction.atomic():
            try:
                # Tạo hoạt động khoa học
                scientific_research = super().create(validated_data)

                # Tính tổng điểm các user khác
                total_point = sum(item.get('point', 0) for item in list_user_data)
                leader_point = scientific_research.time_volume - total_point

                # Gắn request.user là leader với point đã tính
                UserScientificResearch.objects.create(
                    user=user,
                    scientific_research=scientific_research,
                    is_leader=True,
                    point=leader_point
                )

                bulk_data = []
                for item in list_user_data:
                    u = item['id']
                    if u == user:
                        continue
                    point = item.get('point', 0)
                    bulk_data.append(UserScientificResearch(
                        user=u,
                        scientific_research=scientific_research,
                        is_leader=False,
                        point=point
                    ))

                UserScientificResearch.objects.bulk_create(bulk_data)

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
                content_type, _ = mimetypes.guess_type(file_obj.name)
                file_obj.content_type = content_type

                url = clone.upload_file(
                    file_obj=file_obj,
                    type_file=TypeFileEnum.DOCUMENT,
                    folder=FolderEnum.DATA
                )
                data_files.append(url)

            instance.data = data_files
            instance.save()

        return instance
