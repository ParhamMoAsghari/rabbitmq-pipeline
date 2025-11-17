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

