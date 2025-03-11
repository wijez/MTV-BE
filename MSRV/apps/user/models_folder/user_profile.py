from django.db import models
from MSRV.apps.user.models import User
from MSRV.apps.utils.enum_type import DegreeEnum, DepartmentEnum

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    degree = models.CharField(max_length=30, null=False, blank=False, choices=DegreeEnum.choices(),
                            default=DegreeEnum.TS)
    department = models.CharField(max_length=30, null=False, blank=False, choices=DepartmentEnum.choices(),
                            default=DepartmentEnum.INFORMATION_TECHNOLOGY)

    country = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=255, null=False, blank=False)
    nation = models.CharField(max_length=64, null=False, blank=False)
    nationality = models.CharField(max_length=64, null=False, blank=False)
    religion = models.CharField(max_length=64, null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.full_name}"
