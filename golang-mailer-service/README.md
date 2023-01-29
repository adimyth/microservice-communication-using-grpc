## Setup

### Create golang project

```bash
mkdir golang-microservice

cd golang-microservice

go mod init github.com/adimyth/microservice-communication-using-grpc/golang-microservice
```

### Install gRPC

```bash
go get -u google.golang.org/grpc
```

### Install go plugins for protocol compiler

```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.28
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.2

export PATH="$PATH:$(go env GOPATH)/bin"
```

### Install package dependencies

```bash
go get github.com/joho/godotenv
go get github.com/sendgrid/sendgrid-go
```

## Mailer Servie

### 1. Define gRPC service

```protobuf
syntax = "proto3";

package mailer;

// service is a collection of RPC methods.
service MailerService {
    rpc SendMails (SendMailRequest) returns (SendMailResponse) {}
}

message SendMailRequest {
    string receiver = 1;
    string subject = 2;
    string body = 3;
}

message SendMailResponse {
    bool success = 1;
}
```

### 2. Generate gRPC code

```bash
protoc --go_out=. --go-grpc_out=. mailer.proto
```

### 3. Creating the gRPC server

#### 3.1 Implement gRPC service

```go
package main

import (
	"context"
	"fmt"
	"log"
	"net"

	"github.com/adimyth/microservice-communication-using-grpc/golang-mailer-service/mailer"

	"google.golang.org/grpc"
)

// MailerServiceServer is the server for the MailerService service.
type MailerServiceServer struct{}

// SendMails sends an email to the specified receiver with the given subject and body.
func (s *MailerServiceServer) SendMails(ctx context.Context, request *mailer.SendMailRequest) (*mailer.SendMailResponse, error) {

	SendEmail(request.ReceiverEmail, request.ReceiverName, request.Subject, request.Body)
	return &mailer.SendMailResponse{
		Success: true,
	}, nil
}

func main() {
	// Create a listener on TCP port 50051
	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", 50052))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	// Create a gRPC server object
	grpcServer := grpc.NewServer()

	// Attach the MailerService service to the server
	mailer.RegisterMailerServiceServer(grpcServer, &MailerServiceServer{})

	// Serve gRPC Server
	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %s", err)
	}
}
```

**_`request`_**
`request` argument represents the request message that the client sends to the server. In case of `SendOTP` method, request looks like the request message defined in the `.proto` file

**_`context`_**
The `context` argument represents the context of the RPC call. It carries information that can be used to cancel, timeout, or propagate metadata across RPC boundaries. The context can be used to pass information such as the authentication credentials of the client, the deadline for the RPC call, or the trace ID of the RPC call.

The context object has a few key properties:

- `Deadline`: The deadline for the RPC call. If the RPC call takes longer than the deadline, the call will be cancelled and the client will receive a DEADLINE_EXCEEDED error.
- `Cancelled`: A boolean value that indicates whether the RPC call has been cancelled. If the value is True, it means that the RPC call has been cancelled by the client or the server.
- `Err()`: A function that returns the error that caused the RPC call to be cancelled, if any.
- `Value(key interface{}) interface{}`: A function that returns the value associated with the given key in the context. This can be used to pass metadata such as authentication credentials or trace IDs across RPC boundaries.

#### 3.2 Run the gRPC server

```bash
go run server.go
```

### 4. gRPC Client (Postman)

https://user-images.githubusercontent.com/26377913/209468175-d90887df-4cc9-4f75-8c01-f7a86083c0b1.mov

### 5. gRPC client (Golang)

> Consuming the mailer service using a Golang client residing in the same directory

```go
package main

import (
	"context"
	"log"

	"github.com/adimyth/microservice-communication-using-grpc/golang-mailer-service/sendgrid-mailer"
	"google.golang.org/grpc"
)

func main() {
	// Create a connection to the gRPC server using the grpc.Dial function.
	conn, err := grpc.Dial("localhost:50052", grpc.WithInsecure())
	if err != nil {
		log.Fatalf("failed to dial: %v", err)
	}
	defer conn.Close()

	// Create a client for the MailerService service
	client := sendgrid_mailer.NewMailerServiceClient(conn)

	// Set the request parameters
	request := &sendgrid_mailer.SendMailRequest{
		ReceiverEmail: "aditya@fnp.dev",
		ReceiverName:  "adimyth",
		Subject:       "Hello from gRPC",
		Body:          "This is a message from the gRPC client",
	}

	// Use the SendMails method of the MailerService client to send an email to the specified receiver with the given subject and body.

	response, err := client.SendMails(context.Background(), request)
	if err != nil {
		log.Fatalf("failed to send email: %v", err)
	}
	log.Printf("email sent: %v", response.Success)
}
```

### 6. gRPC Client (Python)

> Consuming the mailer service using a Python client residing in the same directory

1. Generate the Python bindings for the gRPC service definition by using the `protoc` compiler with the appropriate plugins. This will create a `.pb` file containing the definitions of the service, request, and response messages, as well as the gRPC stubs needed to call the service.

   ```bash
   mkdir sendgrid_mailer_python

   source ../python_phone_otp_service/.venv/bin/activate

   python3 -m grpc_tools.protoc --proto_path=. --python_out=sendgrid_mailer_python --grpc_python_out=sendgrid_mailer_python mailer.proto
   ```

2. Import the generated module and create a gRPC channel to connect to the gRPC server. Use the service stubs to call the gRPC methods as if they were local functions.

   ```python
   	# Import the generated module and create a gRPC channel
   import sendgrid_mailer_pb2_grpc
   import sendgrid_mailer_pb2
   channel = grpc.insecure_channel('localhost:50052')

   # Create a stub for the MailerService
   stub = sendgrid_mailer_pb2_grpc.MailerServiceStub(channel)

   # Create a request message
   request = sendgrid_mailer_pb2.SendMailRequest(
   	receiver='receiver@example.com',
   	subject='Hello World!',
   	body='This is a test email.'
   )

   # Call the SendMails method using the stub
   response = stub.SendMails(request)

   # Print the response
   print(f"Response received: {response.success}")
   ```

### 7. Structure

```bash
.
├── README.md
├── client-stubs -- contains client codes
│   ├── sendgrid-mailer -- golang client code to consume the mailer service
│   │   └── mailer-client.go
│   └── sendgrid-mailer-python -- python client code to consume the mailer service
│       └── mailer-client.py
├── go.mod
├── go.sum
├── mailer.proto -- gRPC service definition
├── sendgrid-mailer -- contains generated gRPC client and server code for golang
│   ├── mailer.pb.go
│   └── mailer_grpc.pb.go
├── sendgrid_mailer_python -- contains generated gRPC client and server code for python
│   ├── mailer_pb2.py
│   └── mailer_pb2_grpc.py
└── server.go -- gRPC server code
```
