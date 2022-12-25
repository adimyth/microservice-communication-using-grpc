import os
from twilio.rest import Client  # type: ignore
import random
import string
from dotenv import load_dotenv  # type: ignore

load_dotenv()


class TwilioService:
    def __init__(self):
        self.account_ssid = os.environ.get("TWILIO_ACCOUNT_SID")
        self.auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.verification_service_sid = os.environ.get(
            "TWILIO_VERIFICATION_SERVICE_SID"
        )
        self.client = Client(self.account_ssid, self.auth_token)

    def send_otp_to_phone(self, phone_number: str) -> str:
        # send OTP to phone number using twilio
        verification = self.client.verify.services(
            self.verification_service_sid
        ).verifications.create(to=phone_number, channel="sms")
        return verification.sid

    def verify_otp(self, phone_number: str, otp: str) -> bool:
        # verify OTP using twilio
        verification_check = self.client.verify.services(
            self.verification_service_sid
        ).verification_checks.create(to=phone_number, code=otp)
        return verification_check.status == "approved", verification_check.status
