from MSRV.apps.sponsorship_proposal.models import SponsorshipProposal
from MSRV.apps.sponsorship_proposal.views_folder import (
    viewsets
)
from MSRV.apps.sponsorship_proposal.serializers import (
    SponsorshipProposalSerializer
)

class SponsorshipProposalViewSet(viewsets.ModelViewSet):

    queryset = SponsorshipProposal.objects.all()
    serializer_class = SponsorshipProposalSerializer
