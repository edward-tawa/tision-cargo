from loguru import logger

from authentication.otp.models.otp_model import OTP


class OTPService:
    @staticmethod
    def generate_and_send_otp(user):
        # 1. Invalidate any existing unused OTPs for this user
        OTP.objects.filter(user=user, is_used=False).update(is_used=True)

        # 2. Create a new OTP (auto-generates 6 digits and sets 10-min expiry via model save())
        otp_obj = OTP.objects.create(user=user)

        # 3. Dispatch SMS (Mocked to console, ready for Africa's Talking / Twilio integration)
        sms_message = f"[TISION CARGO] Your verification code is: {otp_obj.code}. Valid for 10 minutes."

        logger.info("==================================================")
        logger.info(f"SMS GATEWAY MOCK -> Sending to {user.phone_number}")
        logger.info(f"Message: {sms_message}")
        logger.info("==================================================")

        return otp_obj
