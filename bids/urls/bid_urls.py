# bids/urls.py
from rest_framework.routers import DefaultRouter

from bids.views.bid_views import BidViewSet

router = DefaultRouter()
router.register(r"", BidViewSet, basename="bid")
urlpatterns = router.urls
