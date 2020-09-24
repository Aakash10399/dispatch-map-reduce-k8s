FROM alpine:latest

RUN apk update
RUN apk add python3 py-pip --no-cache

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]