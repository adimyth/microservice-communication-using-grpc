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