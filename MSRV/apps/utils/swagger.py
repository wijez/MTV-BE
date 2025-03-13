from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

def swagger_import_users():
    return swagger_auto_schema(
        operation_description="Import danh sách user từ file CSV",
        manual_parameters=[
            openapi.Parameter(
                name="file",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description="Tệp CSV chứa danh sách email cần tạo tài khoản"
            )
        ],
        responses={
            201: openapi.Response("Danh sách user được tạo thành công"),
            400: openapi.Response("Lỗi khi xử lý file")
        }
    )
