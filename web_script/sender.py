import json_checker
from aiogram import Bot
import asyncio

data = json_checker.get_data_for_sender_telegram_bot()
bot = Bot(token=data["token"])


async def send_message_to_user(text):
    await bot.send_message(data["user_id"], text)
    await bot.send_message(data["chat_id"], text)


def send_message(message):
    asyncio.get_event_loop().run_until_complete(send_message_to_user(message))
