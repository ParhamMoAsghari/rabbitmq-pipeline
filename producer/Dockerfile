FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all Python files and scripts
COPY . .

# Ensure wait-for-it.sh is executable
RUN chmod +x wait-for-it.sh

ENV PYTHONUNBUFFERED=1

CMD ["./wait-for-it.sh", "rabbitmq:5672", "--", "python", "producer.py"]
