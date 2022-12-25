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

### 3. Creating the gRPC server

Creating and running a gRPC server is very similar to creating and running a HTTP server. The only difference is that we need to create a gRPC server instead of a HTTP server.

Creating and running `PhoneOTP` server breaks down into 2 steps:

- Implementing the `PhoneOTPService` service interface generated from the `phoneotp.proto` file
- Creating and running a gRPC server to listen for requests from clients and transmit responses

#### 3.1 Implement the `PhoneOTP` gRPC service
