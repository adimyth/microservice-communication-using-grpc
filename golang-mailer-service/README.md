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
