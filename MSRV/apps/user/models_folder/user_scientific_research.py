import uuid
from django.db import models

from MSRV.apps.user.models import User
from MSRV.apps.sr_activities.models import ScientificResearch


class UserScientificResearch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_scientific_research")
    scientific_research = models.ForeignKey(ScientificResearch, on_delete=models.CASCADE, related_name="user_scientific_research")
    point = models.FloatField(default=0)
    is_leader = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
