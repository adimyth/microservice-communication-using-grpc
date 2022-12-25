package main

import (
	"context"
	"fmt"
	"github.com/adimyth/microservice-communication-using-grpc/golang-mailer-service/sendgrid-mailer"
	"log"
	"net"

	"google.golang.org/grpc"

	"os"

	"github.com/joho/godotenv"
	"github.com/sendgrid/sendgrid-go"
	"github.com/sendgrid/sendgrid-go/helpers/mail"
)

// send email using sendgrid
func SendEmail(receiver_email string, receiver_name string, subject string, body string) {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	// Initialise the required mail message variables
	from := mail.NewEmail(os.Getenv("SEND_FROM_NAME"), os.Getenv("SEND_FROM_ADDRESS"))
	to := mail.NewEmail(receiver_name, receiver_email)
	message := mail.NewSingleEmail(from, subject, to, body, "")

	// Attempt to send the email
	client := sendgrid.NewSendClient(os.Getenv("SENDGRID_API_KEY"))
	response, err := client.Send(message)
	if err != nil {
		fmt.Println("Unable to send your email")
		log.Fatal(err)
	}

	// Check if it was sent
	statusCode := response.StatusCode
	if statusCode == 200 || statusCode == 201 || statusCode == 202 {
		fmt.Println("Email sent!")
	}
}

// MailerServiceServer is the server for the MailerService service.
type MailerServiceServer struct {
	sendgrid_mailer.UnimplementedMailerServiceServer
}

// SendMails sends an email to the specified receiver with the given subject and body.
func (s *MailerServiceServer) SendMails(ctx context.Context, request *sendgrid_mailer.SendMailRequest) (*sendgrid_mailer.SendMailResponse, error) {

	SendEmail(request.ReceiverEmail, request.ReceiverName, request.Subject, request.Body)
	return &sendgrid_mailer.SendMailResponse{
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
	sendgrid_mailer.RegisterMailerServiceServer(grpcServer, &MailerServiceServer{})

	// Serve gRPC Server
	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %s", err)
	}
}
