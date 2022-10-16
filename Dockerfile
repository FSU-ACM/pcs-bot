FROM python:3.9-alpine
LABEL maintainer="ACM at FSU <contact@fsu.acm.org>"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ARG REQUIREMENTS=requirements.txt

# Basic dependencies
RUN apk --no-cache add -q \
	git mercurial cloc openssl openssl-dev openssh \
	alpine-sdk bash gettext sudo build-base gnupg linux-headers xz \
	&& rm -rf /var/cache/apk/* 
	
RUN pip install --upgrade pip


# Requirements installation
COPY $REQUIREMENTS /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt \
	&& rm -rf /tmp/requirements.txt \
	&& rm -rf /root/.cache/pip/*

# User and Group setup
RUN addgroup app_user

RUN adduser \
	--disabled-password \
	--no-create-home \
	--ingroup app_user \
	app_user

# App directory setup
RUN mkdir /app \
	&& chown app_user:app_user /app 

WORKDIR /app

USER app_user:app_user

# Copy project to app directory
COPY --chown=app_user:app_user src .

ENTRYPOINT ["python", "bot.py"]
