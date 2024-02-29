# syntax=docker/dockerfile:1
FROM python:3.10-slim-bullseye as production
LABEL maintainer="Daniil Palona2006@yandex.ru>" \
      description="Telegram Bot"

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PATH "/app/scripts:${PATH}"

EXPOSE 80
WORKDIR /app


# Add code & install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

ADD . /app/


CMD ["python3", "main.py"]
