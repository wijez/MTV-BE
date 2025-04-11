import uuid
from django.db import models

from MSRV.apps.utils.enum_type import StatusSREnum
from MSRV.apps.sr_activities.models_folder.scientific_research_activities import ScientificResearchActivity


class ScientificResearch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sr_activities = models.ForeignKey(ScientificResearchActivity, on_delete=models.CASCADE, related_name="scientific_research")
    name = models.CharField(max_length=255, null=False, blank=False)
    number_member = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, null=False, blank=False, choices=StatusSREnum.choices(),
                            default=StatusSREnum.OPEN)
    level = models.CharField(max_length=100)
    quantity = models.IntegerField(null=True, blank=True)
    time_volume = models.IntegerField(null=True, blank=True)
    banner = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "s_research"

    def __str__(self):
        return self.name
