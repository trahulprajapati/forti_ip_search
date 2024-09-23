FROM python:3.9.6-alpine
ARG workdir=/opt/app
ARG app=ip_search
RUN mkdir -p $workdir

WORKDIR $workdir

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

RUN apk add --no-cache linux-headers g++

RUN apk update \
    && apk add gcc python3-dev musl-dev \
    && apk add libffi-dev

COPY ../../. .

RUN pip install --upgrade pip
RUN pip install  --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["uwsgi", "--ini", "/opt/app/config/uwsgi.ini"]
