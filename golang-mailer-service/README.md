## Setup

### Create golang project

```bash
mkdir golang-microservice

cd golang-microservice

go mod init github.com/adimyth/microservice-communication-using-grpc/golang-microservice
```

### Install Protocol Buffers

```bash
go get -u github.com/golang/protobuf/protoc-gen-go
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

### Install dependencies

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

### 3. Implement gRPC service

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

### 4. Run gRPC server

```bash
go run server.go
```

### 5. Test gRPC service using Postman

https://user-images.githubusercontent.com/26377913/209468175-d90887df-4cc9-4f75-8c01-f7a86083c0b1.mov

### 6. gRPC client

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
