import asyncio
import aio_pika
import json
import os
from tracing import setup_tracer
from opentelemetry.propagate import inject

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
QUEUE_NAME = "task_queue"

tracer = setup_tracer("rabbitmq-producer")

async def connect_rabbit():
    while True:
        try:
            connection = await aio_pika.connect_robust(f"amqp://guest:guest@{RABBITMQ_HOST}/")
            print("Connected to RabbitMQ")
            return connection
        except Exception as e:
            print(f"RabbitMQ not ready, retrying in 3s... ({e})")
            await asyncio.sleep(3)

async def main():
    connection = await connect_rabbit()
    async with connection:
        channel = await connection.channel()
        await channel.declare_queue(QUEUE_NAME, durable=True)

        for i in range(50):
            message = {"id": i, "msg": f"hello {i}"}
            json_body = json.dumps(message).encode("utf-8")

            with tracer.start_as_current_span("send_message") as span:
                span.set_attribute("message.id", i)
                span.set_attribute("message.content", message["msg"])

                headers = {}
                inject(headers)  # inject current trace context

                await channel.default_exchange.publish(
                    aio_pika.Message(
                        body=json_body,
                        content_type="application/json",
                        delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                        headers=headers,
                    ),
                    routing_key=QUEUE_NAME,
                )

            print("Sent:", message)
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
