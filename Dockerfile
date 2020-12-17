FROM python:3.7-alpine
RUN apk add --no-cache gcc musl-dev linux-headers
WORKDIR /code
COPY . .
RUN python -m pip install -r requirements.txt
