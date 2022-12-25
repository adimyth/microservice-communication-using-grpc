import grpc  # type: ignore

import phone_otp.phoneotp_pb2 as phoneotp_pb2  # type: ignore
import phone_otp.phoneotp_pb2_grpc as phoneotp_pb2_grpc  # type: ignore


def main(phone_number, otp):
    # Create a connection to the gRPC server
    with grpc.insecure_channel("localhost:50051") as channel:

        # Create a client for the PhoneOTPService service
        stub = phoneotp_pb2_grpc.PhoneOTPServiceStub(channel)

        # send an otp to a phone number
        response = stub.VerifyOTP(phoneotp_pb2.VerifyOTPRequest(phone_number, otp))
        print(f"VerifyOTP response: {response}")


if __name__ == "__main__":
    main(phone_number="9029080380", otp="123456")
