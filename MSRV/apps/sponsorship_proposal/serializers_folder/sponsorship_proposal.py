from MSRV.apps.sponsorship_proposal.models_folder.sponsorship_proposal import SponsorshipProposal
from MSRV.apps.sponsorship_proposal.serializers_folder import serializers


class SponsorshipProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SponsorshipProposal
        fields = '__all__'
