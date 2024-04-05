# syntax=docker/dockerfile:1
FROM python:3.10-slim-bullseye as production
LABEL maintainer="Daniil Palona2006@yandex.ru>" \
      description="Telegram Bot"

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PATH "/app/scripts:${PATH}"

EXPOSE 80
WORKDIR /app

RUN useradd -ms /bin/sh -u 1001 app
USER app


# Add code & install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY --chown=app:app . /app


CMD ["python3", "main.py"]
