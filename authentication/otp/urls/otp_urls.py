from django.urls import path

from authentication.otp.views.request_otp_views import RequestOTPView
from authentication.otp.views.verify_otp_views import VerifyOTPView

urlpatterns = [
    path("request/", RequestOTPView.as_view(), name="request-otp"),
    path("verify/", VerifyOTPView.as_view(), name="verify-otp"),
]
