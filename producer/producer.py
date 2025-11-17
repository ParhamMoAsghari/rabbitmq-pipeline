import asyncio
import aio_pika
import json
import os

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
QUEUE_NAME = "task_queue"


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

        for i in range(100):
            message = {"id": i, "msg": f"hello {i}"}
            print("Sending Message:", message)

            json_body = json.dumps(message).encode("utf-8")

            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=json_body,
                    content_type="application/json",
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=QUEUE_NAME,
            )

            await asyncio.sleep(1)
            print("Sent:", message)

        print("Done sending.")


if __name__ == "__main__":
    asyncio.run(main())
