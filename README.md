# gRPC

https://www.youtube.com/watch?v=eRndYq8iTio


gRPC (Remote Procedure Calls) is a high-performance, open-source universal RPC framework that enables client and server applications to communicate transparently. It supports multiple programming languages, and it is designed to be simple, fast, and efficient.

In gRPC, a client application can directly call a method on a server application on a different machine as if it was a local object. 

1. gRPC is based around the idea of defining a service, specifying the methods that can be called remotely with their parameters and return types.
2. Server implements this interface and runs a gRPC server to handle client calls.
3. Client has a stub that prrovides the same methods as the server. The client uses the stub to make remote calls to the server just like it would localy.

It abstracts away the ccomplexities of making network calls, using different encodings, and handling failure cases.
* Data serialization
* Network communication
* Authentication❓
* Access Control❓
* Handling failures & retries❓
* Exponential backoff❓
* Load balancing❓

Here's how gRPC works:

1. A client application sends a request message to a gRPC server. The request message contains the name of the remote procedure that the client wants to call, along with any necessary parameters.
2. The gRPC server receives the request and invokes the specified procedure.
3. The server processes the request and returns a response message to the client. The response message contains the result of the procedure, or an error message if there was a problem executing the procedure.
4. The client receives the response and processes the result.

gRPC uses a binary encoding called Protocol Buffers (Protobuf) to serialize and transmit data between the client and server. Protobuf is a language- and platform-neutral data serialization format that is highly efficient and easy to use.

> gRPC also has several features that make it well-suited for building distributed systems, such as automatic retries, load balancing, and streaming support.

gRPC can use protocol buffers as both its *Interface Definition Language (IDL) and it's underlying data exchange format*

