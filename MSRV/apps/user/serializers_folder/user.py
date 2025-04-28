import csv
import io

from MSRV.apps.user.serializers_folder import (
    User,
    AppStatus,
    serializers,
    transaction,
    TypeEmailEnum,
)
import pandas as pd
from MSRV.apps.utils.send_email import sent_mail_verification
from MSRV.apps.user.serializers_folder.user_profile import UserProfileSerializer
from MSRV.apps.utils.generate_password import generate_password
from MSRV.apps.user.models_folder.user_profile import UserProfile
import logging
from django.db import IntegrityError

logger = logging.getLogger(__name__)

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


class AdminUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    class Meta:
        model = User
        fields =  ['id','email', 'full_name', 'role', 'is_active', 'profile']
        extra_kwargs = {
            'date_joined': {"read_only": True},
            'password': {"write_only": True, "min_length": 8, "required": False},
            'is_staff': {"default": False}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        if not request or not request.user.role == "ADMIN":
            raise serializers.ValidationError(AppStatus.USER_NOT_FORBIDDEN)

        profile_data = validated_data.pop("profile", {})
        email = validated_data["email"]
        user = User.objects.filter(email=email).first()
        password = generate_password()

        if user and user.is_active:
            raise serializers.ValidationError(AppStatus.EMAIL_ALREADY_EXIST.message)

        try:
            with transaction.atomic():
                if not user:
                    user = User.objects.create_user(password=password, **validated_data)
                else:
                    user.set_password(password)
                    user.save()

                # Create or update profile
                profile, created = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={"base_point": 0, **profile_data}
                )

                if not created:
                    for key, value in profile_data.items():
                        setattr(profile, key, value)
                    if profile.base_point is None:
                        profile.base_point = 0
                    profile.save()

            sent_mail_verification(user=user, type_mail=TypeEmailEnum.REGISTER_FROM_ADMIN, password=password)
            return user

        except Exception as e:
            logger.exception(f"Lỗi khi tạo user {email}: {e}")
            raise serializers.ValidationError(AppStatus.REGISTER_USER_FAIL.message)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if profile_data:
            profile = instance.profile
            profile_serializer = UserProfileSerializer(profile, data=profile_data, partial=True)
            if profile_serializer.is_valid():
                profile_serializer.save()
                profile.save()
            else:
                raise serializers.ValidationError(profile_serializer.errors)

        return instance

    def create_multiple_users(self, uploaded_file):
        request = self.context.get("request")
        if not request or request.user.role != "ADMIN":
            raise serializers.ValidationError(AppStatus.USER_NOT_FORBIDDEN)

        try:
            file_ext = uploaded_file.name.split('.')[-1].lower()

            if file_ext == "csv":
                data = uploaded_file.read().decode("utf-8")
                csv_reader = csv.reader(io.StringIO(data))
                header = next(csv_reader, None)
                data_rows = [row for row in csv_reader]

            elif file_ext in ["xls", "xlsx"]:
                df = pd.read_excel(uploaded_file, dtype=str)
                data_rows = df.values.tolist()

            else:
                raise serializers.ValidationError(AppStatus.ONLY_SUPPORT_CSV_OR_EXCEL.message)

            created_users = []
            errors = []

            with transaction.atomic():
                for idx, row in enumerate(data_rows, start=2):
                    if not row or len(row) < 1:
                        errors.append(f"Dòng {idx} thiếu dữ liệu (cần ít nhất Email)")
                        continue

                    email = str(row[0]).strip()
                    if not email:
                        errors.append(f"Thiếu email ở dòng {idx}")
                        continue

                    user = User.objects.filter(email=email).first()
                    password = generate_password()

                    if user and user.is_active:
                        errors.append(f"Email {email} đã tồn tại.")
                        continue

                    try:
                        if not user:
                            user = User.objects.create_user(email=email, password=password)
                        else:
                            user.set_password(password)
                            user.save()

                        profile, _ = UserProfile.objects.get_or_create(user=user, defaults={'base_point': 0})
                        if profile.base_point is None:
                            profile.base_point = 0
                            profile.save()

                        sent_mail_verification(user=user, type_mail=TypeEmailEnum.REGISTER_FROM_ADMIN,
                                               password=password)

                        created_users.append({
                            "email": email,
                            "password": password,
                        })

                    except IntegrityError as e:
                        logger.warning(f"IntegrityError dòng {idx} ({email}): {e}")
                        errors.append(f"Lỗi dữ liệu ở dòng {idx}: {e}")

                    except Exception as e:
                        logger.exception(f"Lỗi không xác định dòng {idx} ({email}): {e}")
                        errors.append(f"Lỗi không xác định ở dòng {idx}: {str(e)}")

            if errors:
                raise serializers.ValidationError({"errors": errors})

            return {"created_users": created_users}

        except Exception as e:
            logger.exception(f"Lỗi khi xử lý file import: {e}")
            raise serializers.ValidationError(
                {"error": "Lỗi khi xử lý file. Vui lòng kiểm tra định dạng hoặc nội dung file."})


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            if not user.is_active:
                raise serializers.ValidationError(AppStatus.USER_IS_ACTIVE.message)
            self.user = user
        except Exception as e:
            raise serializers.ValidationError(AppStatus.USER_NOT_EXIST.message.update({"error": str(e)}))
        return value

    def send_reset_email(self):
        sent_mail_verification(user=self.user, type_mail=TypeEmailEnum.RESET_PASSWORD)



class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'role', 'is_active', 'date_joined']

