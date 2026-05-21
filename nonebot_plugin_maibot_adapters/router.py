import asyncio

from maim_message import MessageBase, MessageConverter
from maim_message.client import ClientConfig, WebSocketClient
from nonebot import get_bot, get_plugin_config, logger
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment

from .config import Config
from .util import base64_to_image


config = get_plugin_config(Config)


async def message_handler(message, metadata: dict | None = None):
    """Handle messages sent from MaiBot to OneBot."""
    try:
        legacy_message = MessageConverter.from_api_send(message)
        message_info = legacy_message.message_info
        message_segment = legacy_message.message_segment

        group_info = message_info.group_info
        user_info = message_info.user_info
        group_id = group_info.group_id if group_info else None
        user_id = user_info.user_id if user_info else None

        bot: Bot = get_bot()
        message_chain = Message()
        reply_msg_id = None

        segments = (
            message_segment.data
            if message_segment.type == "seglist"
            else [message_segment]
        )

        for segment in segments:
            seg_type = segment.type
            seg_data = segment.data

            if seg_type == "reply":
                reply_msg_id = seg_data
            elif seg_type == "text":
                message_chain += MessageSegment.text(str(seg_data))
            elif seg_type in {"image", "emoji"}:
                image_path = base64_to_image(seg_data)
                message_chain += MessageSegment.image(file=image_path)

        if reply_msg_id:
            message_chain = MessageSegment.reply(reply_msg_id) + message_chain

        if group_id:
            await bot.send_msg(
                message_type="group",
                group_id=int(group_id),
                message=message_chain,
            )
        elif user_id:
            await bot.send_msg(
                message_type="private",
                user_id=int(user_id),
                message=message_chain,
            )

        return {"status": "success"}

    except Exception as e:
        logger.error(f"处理 MaiBot 回调消息时出错: {e}")
        return {"status": "error", "message": str(e)}


class MaimSocketIORouter:
    def __init__(self):
        self.client: WebSocketClient | None = None
        self.connected = asyncio.Event()

    async def run(self):
        client_config = ClientConfig(
            url=config.url,
            api_key=config.api_key,
            platform=config.platfrom,
            on_message=message_handler,
        )
        self.client = WebSocketClient(client_config)
        await self.client.start()

        while True:
            try:
                if not self.client.connected:
                    ok = await self.client.connect()
                    if ok:
                        self.connected.set()
                    else:
                        self.connected.clear()
                await asyncio.sleep(5)
            except asyncio.CancelledError:
                raise
            except Exception as e:
                self.connected.clear()
                logger.error(f"连接 MaiBot Socket.IO 服务失败: {e}")
                await asyncio.sleep(5)

    async def stop(self):
        self.connected.clear()
        if self.client:
            await self.client.stop()

    async def send_message(self, message: MessageBase):
        if not self.client:
            raise RuntimeError("MaiBot Socket.IO client is not started")
        if not self.client.connected:
            await self.client.connect()
        api_message = MessageConverter.to_api_receive(
            message,
            api_key=config.api_key,
            platform=config.platfrom,
        )
        return await self.client.send_message(api_message)


router = MaimSocketIORouter()


async def main():
    try:
        await router.run()
    finally:
        await router.stop()
