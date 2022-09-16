FROM python:3.9-alpine
LABEL maintainer="ACM at FSU <contact@fsu.acm.org>"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ARG REQUIREMENTS=requirements.txt

RUN \
	# basic deps
	apk --no-cache add -q git mercurial cloc openssl openssl-dev openssh alpine-sdk bash gettext sudo build-base gnupg linux-headers xz
	
RUN pip install --upgrade pip

COPY $REQUIREMENTS /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt \
	&& rm -rf /tmp/requirements.txt

# remove caches
RUN rm -rf /root/.cache/pip/* && \
	rm -rf /var/cache/apk/*

# User and Group setup
RUN addgroup \
	app_user

RUN adduser \
	--disabled-password \
	--no-create-home \
	--ingroup app_user \
	 app_user

# App directory setup
RUN mkdir /app

RUN chown app_user:app_user /app 

WORKDIR /app

USER app_user:app_user

# Copy project to app directory
COPY --chown=app_user:app_user src .

ENTRYPOINT ["python", "bot.py"]
