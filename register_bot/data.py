from database.setter import DataBase
from register_bot.states import State


class DataListener:
    def __init__(self):
        self.table: DataBase | None = None
        self.state = State()
        self.iteration = 0
        self.data = []

    def set_state(self, state: State):
        self.reset()
        self.state = state

    def get_text(self):
        message = self.state.messages[self.iteration]
        self.iteration += 1
        return message

    def add_data(self, text: str):
        if not self.state.table:
            return

        self.data.append(text)

    def write_to_database(self):
        self.state.table.add_to_database(self.data)
        self.reset()

    def is_not_exit(self):
        return self.iteration < len(self.state.messages)

    def reset(self):
        self.state = State()
        self.iteration = 0
