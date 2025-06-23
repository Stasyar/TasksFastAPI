import json

import aio_pika


async def handle_message_backwarding(message, channel, data) -> None:
    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps({
                "result": data
            }).encode(),
            correlation_id=message.correlation_id,
        ),
        routing_key=message.reply_to,
    )