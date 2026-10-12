# bids/urls.py
from rest_framework.routers import DefaultRouter

from bids.views.bid_views import BidViewSet
from bids.views.driver_bid_application_views import DriverBidApplicationViewSet

router = DefaultRouter()
router.register(r"bids", BidViewSet, basename="bid")
router.register(
    r"driver-applications", DriverBidApplicationViewSet, basename="driver-application"
)
