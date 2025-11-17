# RabbitMQ Pipeline

A simple asynchronous RabbitMQ pipeline using Python, Docker, and `aio-pika`.

This project demonstrates a **producer-consumer setup**:
- **Producer** publishes JSON messages to a RabbitMQ queue.
- **Multiple consumers** consume messages concurrently and process them asynchronously.

---

## Features

- Python 3.11 + aio-pika for async messaging
- RabbitMQ with management UI
- Dockerized services for easy setup
- `wait-for-it.sh` to ensure RabbitMQ is ready before producer/consumers start
- Scalable consumers (example: 3 replicas in Docker Compose)

---

## Architecture

```

Producer --> RabbitMQ Queue --> Consumer 1
Consumer 2
Consumer 3

````

- Messages are distributed fairly across consumers (prefetch count = 1)
- Consumers simulate asynchronous processing (6s per message in this example)

---

## Getting Started

### Prerequisites

- Docker & Docker Compose installed
- (Optional) Python 3.11 if running scripts locally

### Running the pipeline

1. Clone the repo:
```bash
git clone https://github.com/<yourusername>/rabbitmq-pipeline.git
cd rabbitmq-pipeline
````

2. Start all services:

```bash
docker-compose up --build
```

* RabbitMQ runs on:

  * `localhost:5672` (AMQP)
  * `localhost:15672` (management UI)
* Producer will send 100 messages
* Consumers will process messages concurrently

3. Access RabbitMQ management UI:

```
http://localhost:15672
Username: guest
Password: guest
```

---

## Project Structure

```
rabbitmq-pipeline/
├── docker-compose.yml
├── producer/
│   ├── producer.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── wait-for-it.sh
└── consumer/
    ├── consumer.py
    ├── Dockerfile
    ├── requirements.txt
    └── wait-for-it.sh
```

* `docker-compose.yml` – orchestrates RabbitMQ, producer, and consumers
* `producer/` – producer service code and Dockerfile
* `consumer/` – consumer service code and Dockerfile
* `wait-for-it.sh` – helper script to wait for RabbitMQ to be ready

---

## Scaling Consumers

In `docker-compose.yml`:

```yaml
consumer:
  deploy:
    replicas: 3
```

Change `replicas` to scale the number of consumers dynamically.

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## Notes / Tips

* Ensure `wait-for-it.sh` has **LF line endings** on Windows (`bash\r` errors indicate CRLF)
* Use `.gitattributes` for consistent line endings:

```
*.sh text eol=lf
*.py text eol=lf
* text=auto
```

* Use `docker-compose logs -f` to monitor message flow in real time.
