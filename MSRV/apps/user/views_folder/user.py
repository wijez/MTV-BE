from MSRV.apps.user.views_folder import (
    Response, GenericAPIView, APIView, viewsets, IsAuthenticated, FormParser, MultiPartParser, swagger_auto_schema, openapi, Q
)

from MSRV.apps.user.models import  User
from MSRV.apps.utils.constant import AppStatus
from MSRV.apps.user.serializers import (
    UserSerializer,
    UserProfileSerializer,
    UserRegisterSerializer,
    AdminUserSerializer,
)
from MSRV.apps.utils.role import IsAdminUser
from MSRV.apps.utils.swagger import swagger_import_users
from rest_framework import status


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
    serializer_class = AdminUserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:  # GET, HEAD, OPTIONS...
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def filter_queryset(self, queryset):
        queryset_user = self.request.query_params.get('queryset_user')

        if queryset_user:
            queryset = queryset.filter(
                Q(email__icontains=queryset_user) | Q(full_name__icontains=queryset_user)
            )

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('queryset_user', openapi.IN_QUERY, description="Search by email or full name",
                              type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)



class ImportUsersFromCSV(APIView):
    parser_classes = (MultiPartParser, FormParser)
    @swagger_import_users()
    def post(self, request, *args, **kwargs):

        file = request.FILES.get("file")
        if not file:
            return Response(AppStatus.CSV_FILE_NOT_FOUND.message, status=status.HTTP_400_BAD_REQUEST)

        serializer = AdminUserSerializer(context={"request": request})
        result = serializer.create_multiple_users(file)

        return Response(result, status=status.HTTP_201_CREATED)
