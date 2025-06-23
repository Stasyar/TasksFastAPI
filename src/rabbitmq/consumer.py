import asyncio
import json
import os

import aio_pika

from dotenv import load_dotenv, find_dotenv
from src.services.tasks import TaskService

from services.TasksFastAPI.src.rabbitmq.handlers import handle_message_backwarding

load_dotenv(find_dotenv(".jwt_env"))


RABBITMQ_URL: str = os.environ.get("RABBITMQ_URL")
task_service = TaskService()


async def consume_user_events():
    """
    Consumer that listens for user events and responds with number of tasks in execution
    """
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("user_events", durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        data = json.loads(message.body.decode())
                        user_id = data["user_id"]
                        if data.get("event") == "executing_tasks":
                            executing_tasks_count = await task_service.get_executing_tasks_count_by_id(user_id)

                            if message.reply_to:
                                await handle_message_backwarding(message, channel, executing_tasks_count)

                        elif data.get("event") == "viewing_tasks":
                            viewing_tasks = await task_service.get_viewing_tasks_count_by_id(user_id)

                            if message.reply_to:
                                await handle_message_backwarding(message, channel, viewing_tasks)

                    except Exception as e:
                        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(consume_user_events())
