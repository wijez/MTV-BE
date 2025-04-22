from django.db import models
from MSRV.apps.user.models import User
from MSRV.apps.utils.enum_type import DegreeEnum, DepartmentEnum


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    degree = models.CharField(max_length=30, null=False, blank=False, choices=DegreeEnum.choices(),
                            default=DegreeEnum.TS)
    department = models.CharField(max_length=30, null=False, blank=False, choices=DepartmentEnum.choices(),
                            default=DepartmentEnum.INFORMATION_TECHNOLOGY)
    base_point = models.IntegerField(default=0)
    country = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=255, null=False, blank=False)
    nation = models.CharField(max_length=64, null=False, blank=False)
    nationality = models.CharField(max_length=64, null=False, blank=False)
    religion = models.CharField(max_length=64, null=False, blank=False)
    avatar = models.CharField(max_length=255, null=True, blank=True, default=None)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.full_name}"

    def calculate_base_point(self):
        mapping = {
            'UN_TS_III': 600,
            'TS_III': 650,
            'UN_TS_II': 650,
            'TS_II': 750,
            'TS': 750,
            'PGS': 800,
            'GS': 850
        }
        return mapping.get(str(self.degree).upper(), 0)

    def save(self, *args, **kwargs):
        self.base_point = self.calculate_base_point()
        super().save(*args, **kwargs)