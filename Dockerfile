FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /app

COPY ./app /app

RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r /app/requirements.txt

ENTRYPOINT ["python3"]
CMD ["app.py"]

