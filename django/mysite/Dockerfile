# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.8-alpine AS builder
EXPOSE 8000
WORKDIR /mysite 
COPY requirements.txt /mysite
RUN apk add gcc musl-dev
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
RUN apk add npm
RUN npm install sqlite3

COPY . /mysite 
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]

FROM builder as dev-envs
RUN <<EOF
apk update
apk add git
EOF

RUN <<EOF
addgroup -S docker
adduser -S --shell /bin/bash --ingroup docker vscode
EOF
# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /

CMD ["manage.py", "runserver", "0.0.0.0:8000"]
