FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN chmod +x /app/router.py

RUN apt-get update && apt-get install -y iproute2 iputils-ping net-tools

CMD ["python","router.py"]