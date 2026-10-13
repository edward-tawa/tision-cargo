from rest_framework.routers import DefaultRouter

from bookings.views.booking_views import BookingViewSet

router = DefaultRouter()
router.register(r"", BookingViewSet, basename="booking")
urlpatterns = router.urls
