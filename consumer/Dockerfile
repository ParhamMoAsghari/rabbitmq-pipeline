FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY consumer.py wait-for-it.sh ./
RUN chmod +x wait-for-it.sh

ENV PYTHONUNBUFFERED=1

CMD ["./wait-for-it.sh", "rabbitmq:5672", "--", "python", "consumer.py"]
