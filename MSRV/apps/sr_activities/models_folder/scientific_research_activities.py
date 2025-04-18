import uuid
from django.db import models
from MSRV.apps.utils.enum_type import GroupEnum


class ScientificResearchActivity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.CharField(max_length=50, null=False, blank=False, choices=GroupEnum.choices(),
                            default=GroupEnum.RESEARCH_PROJECTS)
    content = models.TextField()
    input = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sr_activities"

    def __str__(self):
        return f"{self.group} - {self.content[:50]}"
