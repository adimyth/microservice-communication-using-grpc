from concurrent import futures
import grpc  # type: ignore
from utils import TwilioService
import phone_otp.phoneotp_pb2 as phoneotp_pb2  # type: ignore
import phone_otp.phoneotp_pb2_grpc as phoneotp_pb2_grpc  # type: ignore


class PhoneOTPService(phoneotp_pb2_grpc.PhoneOTPServiceServicer):
    def __init__(self):
        self.twilio_service = TwilioService()

    def SendOTP(self, request, context):
        message_id = self.twilio_service.send_otp_to_phone(request.phone_number)
        if message_id is None:
            return phoneotp_pb2.SendOTPResponse(success=False)
        print(f"OTP sent to phone number: {request.phone_number}")
        return phoneotp_pb2.SendOTPResponse(success=True)

    def VerifyOTP(self, request, context):
        verified, status = self.twilio_service.verify_otp(request.phone_number, request.otp)
        return phoneotp_pb2.VerifyOTPResponse(success=verified, status=status)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    phoneotp_pb2_grpc.add_PhoneOTPServiceServicer_to_server(PhoneOTPService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
