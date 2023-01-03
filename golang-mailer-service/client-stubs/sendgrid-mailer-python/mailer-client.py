import sys

sys.path.append(".")

import grpc  # type: ignore
import sendgrid_mailer_python.mailer_pb2 as sendgrid_mailer_pb2  # type: ignore
import sendgrid_mailer_python.mailer_pb2_grpc as sendgrid_mailer_pb2_grpc  # type: ignore


def main():
    channel = grpc.insecure_channel("localhost:50052")

    # Create a stub for the MailerService
    stub = sendgrid_mailer_pb2_grpc.MailerServiceStub(channel)

    # Create a request message
    request = sendgrid_mailer_pb2.SendMailRequest(
        receiver_email="RECEIVER_EMAIL",
        receiver_name="RECEIVER_NAME",
        subject="Hello World!",
        body="""
        This is a test email sent using gRPC.

        You can check out my project here - https://github.com/adimyth/microservice-communication-using-grpc

        Thanks for your time! Let me know if you have any questions.

        Best,
        Aditya
        """,
    )

    # Call the SendMails method using the stub
    response = stub.SendMails(request)

    # Print the response
    print(f"Response received: {response.success}")


if __name__ == "__main__":
    main()
