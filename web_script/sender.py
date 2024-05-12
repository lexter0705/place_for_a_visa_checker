import json_checker
from aiogram import Bot
import asyncio

data = json_checker.get_data_for_sender_telegram_bot()
bot = Bot(token=data["token"])


async def send_message_async(message: str, user_id: int):
    await bot.send_message(user_id, message)


def send_message(message: str, user_id: int):
    asyncio.get_event_loop().run_until_complete(send_message_async(message, user_id))
