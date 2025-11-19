import asyncio
import aio_pika
import json
import os
from tracing import setup_tracer
from opentelemetry.propagate import extract

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
QUEUE_NAME = "task_queue"

tracer = setup_tracer("rabbitmq-consumer")

async def connect_rabbit():
    while True:
        try:
            connection = await aio_pika.connect_robust(f"amqp://guest:guest@{RABBITMQ_HOST}/")
            print("Connected to RabbitMQ")
            return connection
        except Exception as e:
            print(f"RabbitMQ not ready, retrying in 3s... ({e})")
            await asyncio.sleep(3)

async def process_message(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        data = json.loads(message.body.decode())

        # Extract trace context from message headers
        ctx = extract(message.headers or {})

        with tracer.start_as_current_span("process_message", context=ctx) as span:
            span.set_attribute("message.id", data.get("id"))
            span.set_attribute("message.content", data.get("msg"))
            print("Received:", data)
            await asyncio.sleep(2)  # simulate processing
            print("Processed:", data)

async def main():
    connection = await connect_rabbit()
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)
        await queue.consume(process_message)
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
