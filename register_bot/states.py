from database.setter import DataBase, UserTable, BlsTable
import json_checker


class State:
    table: DataBase | None = None
    messages: list = []


class UserState(State):
    table = UserTable()
    messages = json_checker.get_data_for_telegram_bot()["user_messages"]


class BotState(State):
    table = BlsTable()
    messages = json_checker.get_data_for_telegram_bot()["bot_messages"]
