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


async def process_message(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        data = json.loads(message.body.decode())
        print("Received:", data)

        # Simulate async processing
        await asyncio.sleep(6)

        print("Processed:", data)


async def main():
    connection = await connect_rabbit()

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        queue = await channel.declare_queue(QUEUE_NAME, durable=True)

        print(" [*] Waiting for messages …")

        await queue.consume(process_message)

        # Keep the consumer running forever
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
