from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from MSRV.apps.user.views_folder import (
    Response, GenericAPIView, APIView, viewsets,
)

from MSRV.apps.user.models import  User
from MSRV.apps.utils.constant import AppStatus
from MSRV.apps.user.serializers import (
    UserSerializer,
    UserProfileSerializer,
    UserRegisterSerializer,
    AdminUserSerializer,
    CustomTokenObtainPairSerializer,
    PasswordResetSerializer,
)
from MSRV.apps.utils.role import IsAdminUser
from MSRV.apps.utils.swagger import swagger_import_users
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi 

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
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, *args, **kwargs):
        profile = request.user.profile
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            profile = serializer.save()
            return Response(UserSerializer(profile.user).data)
        return Response(serializer.errors, status=400)


class AdminUserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = AdminUserSerializer
    queryset = User.objects.all()


class ImportUsersFromCSV(APIView):
    parser_classes = (MultiPartParser, FormParser)
    @swagger_import_users()
    def post(self, request, *args, **kwargs):
        """Nhận file CSV và tạo nhiều user."""
        file = request.FILES.get("file")
        if not file:
            return Response(AppStatus.CSV_FILE_NOT_FOUND.message, status=status.HTTP_400_BAD_REQUEST)

        serializer = AdminUserSerializer(context={"request": request})
        result = serializer.create_multiple_users(file)

        return Response(result, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer

    @swagger_auto_schema(request_body=PasswordResetSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.send_reset_email()
            return Response({"message": "Password reset email sent successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSearchView(APIView):
    @swagger_auto_schema(
        operation_summary="Search users by email or full name",
        manual_parameters=[
            openapi.Parameter(
                'q',
                openapi.IN_QUERY,
                description="Email or full name to search",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def get(self, request):
        query = request.query_params.get('q', None)
        if not query:
            return Response({"detail": "Missing search parameter 'q'."}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(
            Q(email__icontains=query) | Q(full_name__icontains=query),
            soft_delete=False
        )
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)