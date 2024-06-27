FROM golang:1.22.4 as builder

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY . /app

CMD ["sh", "-c", "CGO_ENABLED=0 GOOS=linux go build -v -a -installsuffix cgo -o backend . && ./backend"]

