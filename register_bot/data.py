from database.setter import DataBase
from register_bot.states import State


class DataListener:
    def __init__(self):
        self.__table: DataBase | None = None
        self.__state: State | None = None
        self.__iteration = 0
        self.__data = {"email": "lexter29072007@gmail.com",
                     "pass_account": "Ter29072007!",
                     "proxy_ip_port": "",
                     "proxy_login": "",
                     "proxy_password": ""}

    def set_state(self, state: State):
        self.reset()
        self.__state = state

    def get_message(self) -> dict:
        message = self.__state.messages[self.__iteration]
        self.__iteration += 1
        return message

    def add_data(self, text: str) -> bool:
        if not self.__state.table:
            return False

        if not self.__state.columns:
            return False

        if not self.__state.messages:
            return False

        self.__data[self.__state.columns[self.__iteration - 1]] = text
        return True

    def write_to_database(self):
        self.__state.table.add_to_database(self.__data)
        self.reset()

    def is_not_exit(self):
        return self.__iteration < len(self.__state.messages)

    def reset(self):
        self.__state = None
        self.__iteration = 0
