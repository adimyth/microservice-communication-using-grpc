import sys

sys.path.append(".")

import grpc  # type: ignore

import phone_otp.phoneotp_pb2 as phoneotp_pb2  # type: ignore
import phone_otp.phoneotp_pb2_grpc as phoneotp_pb2_grpc  # type: ignore


def main(phone_number):
    # Create a connection to the gRPC server
    with grpc.insecure_channel("localhost:50051") as channel:

        # Create a client for the PhoneOTPService service
        stub = phoneotp_pb2_grpc.PhoneOTPServiceStub(channel)

        # send an otp to a phone number
        # phone number format should be PINCODE + SPACE + PHONE_NUMBER
        response = stub.SendOTP(
            phoneotp_pb2.SendOTPRequest(phone_number=phone_number)
        )
        print(f"SendOTP response: {response}")


if __name__ == "__main__":
    main("YOUR PHONE NUMBER")
