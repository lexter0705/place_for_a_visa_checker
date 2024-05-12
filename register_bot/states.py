from database.setter import DataBase, UserTable, BlsTable
from json_checker import get_data_for_telegram_bot


class State:
    table: DataBase | None = None
    messages: list = []
    columns: list = []


class NewCheckerState(State):
    table = UserTable()
    messages = get_data_for_telegram_bot()["user_messages"]
    columns = get_data_for_telegram_bot()["user_columns"]
