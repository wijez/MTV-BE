import uuid
from django.db import models

from MSRV.apps.utils.enum_type import StatusSPEnum
from MSRV.apps.sr_activities.models_folder.scientific_research import ScientificResearch


class SponsorshipProposal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    s_research = models.ForeignKey(ScientificResearch, on_delete=models.CASCADE, related_name="sponsorship_proposal")
    context = models.TextField()
    funding = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, null=False, blank=False, choices=StatusSPEnum.choices(),
                            default=StatusSPEnum.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sponsorship_proposal"

    def __str__(self):
        return f"sp_{self.s_research.name}"
