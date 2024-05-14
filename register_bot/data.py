from database.setter import DataBase
from register_bot.states import State


class DataListener:
    def __init__(self):
        self.table: DataBase | None = None
        self.state: State | None = None
        self.iteration = 0
        self.data = {"email": "lexter29072007@gmail.com",
                     "pass_account": "Ter29072007",
                     "proxy_ip_port": "",
                     "proxy_login": "",
                     "proxy_password": ""}

    def set_state(self, state: State):
        self.reset()
        self.state = state

    def get_message(self) -> dict:
        message = self.state.messages[self.iteration]
        self.iteration += 1
        return message

    def add_data(self, text: str) -> bool:
        if not self.state.table:
            return False

        if not self.state.columns:
            return False

        if not self.state.messages:
            return False

        self.data[self.state.columns[self.iteration - 1]] = text
        return True

    def write_to_database(self):
        self.state.table.add_to_database(self.data)
        self.reset()

    def is_not_exit(self):
        return self.iteration < len(self.state.messages)

    def reset(self):
        self.state = None
        self.iteration = 0
