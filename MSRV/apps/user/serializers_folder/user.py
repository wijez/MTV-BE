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
    profile = UserProfileSerializer( read_only=True)

    class Meta:
        model = User
        fields =  ['id','email', 'full_name', 'role', 'is_active', 'date_joined', 'profile']
        extra_kwargs = {
            'password': {"write_only": True, "min_length": 8, "required": False},
            'is_staff': {"default": False}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        if not request or not request.user.role == "ADMIN":
            raise serializers.ValidationError(AppStatus.USER_NOT_FORBIDDEN)

        email = validated_data["email"]
        user = User.objects.filter(email=email).first()

        if user and user.is_active:
            raise serializers.ValidationError(AppStatus.EMAIL_ALREADY_EXIST.message)

        password = generate_password()

        try:
            with transaction.atomic():
                if not user:
                    user = User.objects.create_user(password=password, **validated_data)
                else:
                    user.set_password(password)
                    user.save()

            sent_mail_verification(user=user, type_mail=TypeEmailEnum.REGISTER_FROM_ADMIN, password=password)

            return user

        except Exception as e:
            raise serializers.ValidationError(AppStatus.REGISTER_USER_FAIL.message)

    def update(self, instance, validated_data):
        """Cho phép cập nhật User và UserProfile"""
        profile_data = validated_data.pop("profile", None)

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if profile_data:
                profile_serializer = UserProfileSerializer(instance.profile, data=profile_data, partial=True)
                if profile_serializer.is_valid():
                    profile_serializer.save()
                else:
                    raise serializers.ValidationError(profile_serializer.errors)

        return instance

    def create_multiple_users(self, uploaded_file):
        """Xử lý file CSV hoặc XLSX để tạo nhiều tài khoản user."""
        request = self.context.get("request")
        if not request or request.user.role != "ADMIN":
            raise serializers.ValidationError(AppStatus.USER_NOT_FORBIDDEN)

        try:
            file_ext = uploaded_file.name.split('.')[-1].lower()  # Lấy phần mở rộng file

            if file_ext == "csv":
                # Đọc file CSV
                data = uploaded_file.read().decode("utf-8")
                csv_reader = csv.reader(io.StringIO(data))
                next(csv_reader, None)  # Bỏ qua dòng header nếu S
                data_rows = [row for row in csv_reader]

            elif file_ext in ["xls", "xlsx"]:
                # Đọc file Excel
                df = pd.read_excel(uploaded_file, dtype=str)
                data_rows = df.values.tolist()  # Chuyển DataFrame thành danh sách

            else:
                raise serializers.ValidationError("Chỉ hỗ trợ file CSV hoặc Excel (XLS/XLSX)")

            created_users = []
            errors = []

            with transaction.atomic():
                for idx, row in enumerate(data_rows, start=1):
                    if not row or len(row) < 1:
                        continue

                    email = str(row[0]).strip()  # Lấy email từ cột đầu tiên

                    if not email:
                        errors.append(f"Thiếu email ở dòng {idx}")
                        continue

                    user = User.objects.filter(email=email).first()

                    if user and user.is_active:
                        errors.append(f"Email {email} đã tồn tại.")
                        continue

                    password = generate_password()
                    if not user:
                        user = User.objects.create_user(email=email, password=password)
                    else:
                        user.set_password(password)
                        user.save()

                    sent_mail_verification(user=user, type_mail=TypeEmailEnum.REGISTER_FROM_ADMIN, password=password)
                    created_users.append({
                        "email": email,
                        "password": password,
                    })

                if errors:
                    raise serializers.ValidationError({"errors": errors})

            return {"created_users": created_users}

        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            if not user.is_active:
                raise serializers.ValidationError("User account is inactive.")
            self.user = user
        except User.DoesNotExist:
            raise serializers.ValidationError("No user is associated with this email.")
        return value

    def send_reset_email(self):
        sent_mail_verification(user=self.user, type_mail=TypeEmailEnum.RESET_PASSWORD)



class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'role', 'is_active', 'date_joined']

