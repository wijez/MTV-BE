import uuid
from django.db import models
from MSRV.apps.utils.enum_type import GroupEnum


class ScientificResearchActivity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.CharField(max_length=50, null=False, blank=False, choices=GroupEnum.choices(),
                            default=GroupEnum.RESEARCH_PROJECTS)
    content = models.TextField()
    conversion_time = models.IntegerField()
    proof = models.CharField(max_length=255)
    note = models.TextField(blank=True, null=True)
    input = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sr_activities"  # Định danh tên bảng

    def __str__(self):
        return f"{self.group} - {self.content[:50]}"  # Hiển thị nội dung ngắn gọn
