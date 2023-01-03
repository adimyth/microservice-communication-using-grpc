package main

import (
	"context"
	"log"

	"github.com/adimyth/microservice-communication-using-grpc/golang-mailer-service/sendgrid-mailer"
	"google.golang.org/grpc"
)

func main() {
	// Create a connection to the gRPC server
	conn, err := grpc.Dial("localhost:50052", grpc.WithInsecure())
	if err != nil {
		log.Fatalf("failed to dial: %v", err)
	}
	defer conn.Close()

	// Create a client for the MailerService service
	client := sendgrid_mailer.NewMailerServiceClient(conn)

	// Set the request parameters
	request := &sendgrid_mailer.SendMailRequest{
		ReceiverEmail: "RECEIVER_EMAIL",
		ReceiverName:  "RECEIVER_NAME",
		Subject:       "Hello from gRPC",
		Body: `
		This is a message from the gRPC client.

		You can check out my project here - https://github.com/adimyth/microservice-communication-using-grpc
		
        Thanks for your time! Let me know if you have any questions.

        Best,
        Aditya
		`,
	}

	// Send the email
	response, err := client.SendMails(context.Background(), request)
	if err != nil {
		log.Fatalf("failed to send email: %v", err)
	}
	log.Printf("email sent: %v", response.Success)
}
