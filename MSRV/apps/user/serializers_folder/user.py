from MSRV.apps.user.serializers_folder import (
    User,
    AppStatus,
    serializers,
    transaction,
    TypeEmailEnum,
)
from MSRV.apps.utils.send_email import sent_mail_verification
from MSRV.apps.user.serializers_folder.user_profile import UserProfileSerializer

class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, "min_length": 8}}

    def create(self, validated_data):
        user = User.objects.filter(email=validated_data["email"]).first()
        if user and user.is_active:
            raise serializers.ValidationError(AppStatus.EMAIL_ALREADY_EXIST.message)

        with transaction.atomic():
            try:
                if not user:
                    user = User.objects.create_user(**validated_data)
                    sent_mail_verification(user=user, type_mail=TypeEmailEnum.REGISTER)
            except Exception as e:
                print(e)
                transaction.rollback()
                raise serializers.ValidationError(AppStatus.REGISTER_USER_FAIL.message)
        return user


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}, 'verify_code': {'write_only': True}}

    def get_fields(self):
        fields = super().get_fields()
        fields.pop('groups', None)
        fields.pop('user_permissions', None)
        return fields
