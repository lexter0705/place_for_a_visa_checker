import json_checker
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from register_bot.data import DataListener
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.filters import CommandStart
from register_bot.states import UserState, BotState
import asyncio

data = json_checker.get_data_for_telegram_bot()
bot = Bot(token=data["token"])
print(data["token"])
dp = Dispatcher()

main_buttons = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="New user", callback_data="user"),
                      InlineKeyboardButton(text="New bot", callback_data="bot")]])

data_listener = DataListener()
start_text = data["start_text"]


@dp.message(CommandStart())
async def start_command_answer(message: Message):
    await message.reply(text=start_text, reply_markup=main_buttons)


@dp.callback_query(lambda c: c.data == "user")
async def start_listen(callback: CallbackQuery):
    data_listener.reset()
    data_listener.set_state(UserState())
    text = data_listener.get_text()
    print(data_listener.state.table.get_columns_name())
    await bot.send_message(callback.from_user.id, text)


@dp.callback_query(lambda c: c.data == "bot")
async def start_listen(callback: CallbackQuery):
    data_listener.reset()
    data_listener.set_state(BotState())
    text = data_listener.get_text()
    await bot.send_message(callback.from_user.id, text)


@dp.message()
async def get_answer(message: Message):
    if message.text == "/start":
        return
    data_listener.add_data(message.text)
    if data_listener.is_not_exit():
        await message.reply(data_listener.get_text())
    else:
        data_listener.write_to_database()
        await message.reply("Ответы записан!")


async def run():
    await dp.start_polling(bot)


def start():
    asyncio.run(run())
