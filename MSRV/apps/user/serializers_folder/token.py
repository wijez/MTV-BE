from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()

class CustomTokenVerifySerializer(TokenVerifySerializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        data = {}
        token = attrs['token']
        email = attrs['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Không tìm thấy người dùng với email này")

        if token == user.verify_code and user.is_active is False:
            user.is_active = True
            user.save()
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token