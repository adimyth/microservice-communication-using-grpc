## Managing Python dependencies

### Create virutal environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip3 install --upgrade pip
pip3 install --upgrade setuptools

pip3 install -r requirements.txt
```

## Phone OTP Service

We will be using [Twilio](https://www.twilio.com/) to send and verify OTPs. You will need to create a Twilio account and get the following credentials:

- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`
- `TWILIO_VERIFICATION_SERVICE_SID`

### 1. Define the gRPC service

The gRPC service is defined in the `phoneotp.proto` file. The `phoneotp.proto` file contains the definition of the gRPC service and the request and response messages.

```protobuf
syntax = "proto3";

package phoneotp;

// service is a collection of RPC methods.
// RPC methods accept a single request message and return a single response message.
service PhoneOTPService {
    rpc SendOTP (SendOTPRequest) returns (SendOTPResponse) {}
    rpc VerifyOTP (VerifyOTPRequest) returns (VerifyOTPResponse) {}
}

// protobuf data is structured as messages. message is a small logical record of information containing a series of name-value pairs called fields.
message SendOTPRequest {
    string phone_number = 1;
}

message SendOTPResponse {
    bool success = 1;
}

message VerifyOTPRequest {
    string phone_number = 1;
    string otp = 2;
}

message VerifyOTPResponse {
    bool success = 1;
    string status = 2;
}
```

### 2. Generate the gRPC code

The gRPC code is generated from the `phoneotp.proto` file. The `phoneotp.proto` file contains the definition of the gRPC service and the request and response messages.

```bash
mkdir phone_otp

python3 -m grpc_tools.protoc -I . --python_out=phone_otp --grpc_python_out=phone_otp phoneotp.proto
```

- `phoneotp_pb2_grpc::PhoneOTPServiceStub` - Used by client to invoke PhoneOTPService methods
- `phoneotp_pb2_grpc::PhoneOTPServiceServicer` - Defines the interface for implementation of the PhoneOTPservice. Used by server to implement PhoneOTPService methods
- `phoneotp_pb2_grpc::add_PhoneOTPServiceServicer_to_server` - Used by server to register the PhoneOTPService implementation to a `grpc.Server` instance. **_Basically attaches the server implementation to grpc server._**
- `phoneotp_pb2::SendOTPRequest` - Request message for SendOTP method
- `phoneotp_pb2::SendOTPResponse` - Response message for SendOTP method

> **Note**
> You will have to change line 5 in `phoneotp_pb2_grpc.py` from `import phoneotp_pb2 as phoneotp__pb2` to `import phone_otp.phoneotp_pb2 as phoneotp__pb2`

### 3. Creating the gRPC server

Creating and running a gRPC server is very similar to creating and running a HTTP server. The only difference is that we need to create a gRPC server instead of a HTTP server.

Creating and running `PhoneOTP` server breaks down into 2 steps:

- Implementing the `PhoneOTPService` service interface generated from the `phoneotp.proto` file
- Creating and running a gRPC server to listen for requests from clients and transmit responses

#### 3.1 Implement the `PhoneOTP` gRPC service

```python
from concurrent import futures
import grpc  # type: ignore
from utils import TwilioService
import phone_otp.phoneotp_pb2 as phoneotp_pb2  # type: ignore
import phone_otp.phoneotp_pb2_grpc as phoneotp_pb2_grpc  # type: ignore


class PhoneOTPService(phoneotp_pb2_grpc.PhoneOTPServiceServicer):
    def __init__(self):
        # a helper class to send and verify OTPs
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
```

#### 3.2 Run the server

```bash
# copy the .env.example file to .env and update the values
cp .env.example .env

# activate the virtual environment
source .venv/bin/activate

# run the server
python3 server.py
```

### 4. Interacting with the gRPC server using Postman (as a gRPC client)

https://user-images.githubusercontent.com/26377913/209463377-796a7c7a-c7a3-4ee5-87b2-3c4ccc99c7d9.mov
