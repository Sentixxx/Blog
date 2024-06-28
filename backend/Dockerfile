FROM golang:1.22.4 as builder

WORKDIR /go/src/WEB

COPY . /go/src/WEB/


RUN go get github.com/astaxie/beego && go install github.com/beego/bee/v2@latest && go get -u github.com/lib/pq

EXPOSE 8090

RUN go get backend

CMD ["sh"]

