# permissions, action, Response, GenericAPIView, GenericViewSet,
from django.db.models import Q

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import mixins, permissions

from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import LimitOffsetPagination

from rest_framework.views import APIView
from rest_framework import viewsets, filters
