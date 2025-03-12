from rest_framework.permissions import IsAuthenticated

from MSRV.apps.user.views_folder import (
    Response, GenericAPIView
)

from MSRV.apps.user.models import  User
from MSRV.apps.utils.constant import AppStatus
from MSRV.apps.user.serializers import (
    UserSerializer,
    UserProfileSerializer,
    UserRegisterSerializer
)


class RegisterViewSet(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(AppStatus.REGISTER_USER_SUCCESS.message)
        else:
            user = User.objects.filter(email=serializer.data['email']).first()
            if user and not user.is_active:
                user.set_password(serializer.data['password'])
                user.full_name = serializer.data['full_name']
                user.save()
                return Response(AppStatus.REGISTER_USER_SUCCESS.message)
            return Response(serializer.errors)


class UserDetailViewSet(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class UpdateUserViewSet(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def put(self, request, *args, **kwargs):
        profile = request.user.profile
        serializer = self.get_serializer(profile, data=request.data)
        if serializer.is_valid():
            profile = serializer.save()
            return Response(UserSerializer(profile.user).data)
        return Response(serializer.errors)
