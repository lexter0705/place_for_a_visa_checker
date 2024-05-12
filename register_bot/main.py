import json_checker
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from register_bot.data import DataListener
from database.setter import UserTable
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.filters import CommandStart
from register_bot.states import NewCheckerState
import asyncio

data = json_checker.get_data_for_telegram_bot()
bot = Bot(token=data["token"])
dp = Dispatcher()
main_buttons = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Новая получасовая проверка", callback_data="new_checker")]])
data_listeners = {}
user_table = UserTable()
start_text = data["start_text"]
last_message: Message | None = None


@dp.message(CommandStart())
async def start_command_answer(message: Message):
    register_new_user(message)
    init_data_listener(message.from_user.id)
    await message.reply(text=start_text, reply_markup=main_buttons)


def register_new_user(message: Message):
    if user_table.select_user(message.from_user.id):
        return

    user = {"id": message.from_user.id,
            "name": message.from_user.username,
            "count_of_checked": 0,
            "is_height_priority": False}
    user_table.add_to_database(user)


def init_data_listener(user_id: int):
    data_listeners[user_id] = DataListener()


@dp.callback_query(lambda c: c.data == "new_checker")
async def start_listen(callback: CallbackQuery):
    data_listener = data_listeners[callback.from_user.id]
    data_listener.reset()
    data_listener.set_state(NewCheckerState())
    message = data_listener.get_message()
    markup = create_buttons(message["buttons"])
    await bot.send_message(callback.from_user.id, message["text"], reply_markup=markup)


@dp.callback_query(lambda c: c.data != "new_checker")
async def get_answer(callback: CallbackQuery):
    data_listener = data_listeners[callback.from_user.id]
    data_listener.add_data(callback.data)
    if data_listener.is_not_exit():
        message = data_listener.get_message()
        markup = create_buttons(message["buttons"])
        await bot.send_message(callback.from_user.id, message["text"], reply_markup=markup)
    else:
        data_listener.write_to_database()
        await bot.send_message(callback.from_user.id, "Новый проверяющий создан!")


def create_buttons(buttons_text: list[str]) -> InlineKeyboardMarkup:
    keyboard_list = []
    row = []
    print("key")
    for i in range(len(buttons_text)):
        if i % 2 == 0 and i != 0:
            keyboard_list.append(row)
            row = []

        row.append(InlineKeyboardButton(text=buttons_text[i], callback_data=buttons_text[i]))

    keyboard_list.append(row)
    buttons = InlineKeyboardMarkup(inline_keyboard=keyboard_list)
    return buttons


async def run():
    await dp.start_polling(bot)


def start():
    asyncio.run(run())
