from MSRV.apps.sponsorship_proposal.routers import (
    include, path, DefaultRouter
)
from MSRV.apps.sponsorship_proposal.views import (
    SponsorshipProposalViewSet
)

router = DefaultRouter(trailing_slash=False,)
router.register('', SponsorshipProposalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
