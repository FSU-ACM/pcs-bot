FROM gorialis/discord.py:alpine-minimal
LABEL maintainer="ACM at FSU <contact@fsu.acm.org>"

WORKDIR /app

COPY ./src .

CMD ["python", "bot.py"]
