from rest_framework import serializers
from rest_framework.response import Response

from django.db import transaction

from MSRV.apps.user.models import *
from MSRV.apps.utils.constant import AppStatus
from MSRV.apps.utils.enum_type import TypeEmailEnum

