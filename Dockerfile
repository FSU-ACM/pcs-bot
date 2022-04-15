FROM gorialis/discord.py:alpine-minimal
LABEL maintainer="ACM at FSU <contestdev@fsu.acm.org>"

WORKDIR /app

COPY ./src .

CMD ["python", "bot.py"]
