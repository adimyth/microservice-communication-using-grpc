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
