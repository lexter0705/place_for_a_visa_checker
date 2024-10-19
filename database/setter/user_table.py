from database.setter.base_setter import DataBase
from sqlalchemy import select, update
from database.creator import Users


class UserTable(DataBase):
    def __init__(self):
        super().__init__(Users)

    def get_users_with_high_priority(self):
        table_data = self.conn.execute(select(self.table).where(self.table.is_height_priority is True)).all()
        return table_data

    def get_users_with_low_priority(self):
        table_data = self.conn.execute(select(self.table).where(self.table.is_height_priority is False)).all()
        return table_data

    def select_user(self, user_id: int):
        table_data = self.conn.execute(select(self.table).where(self.table.id == user_id)).first()
        return table_data

    def get_user_count_checks(self, user_id: int):
        table_data = self.conn.execute(select(self.table.count_of_checked).where(self.table.id == user_id)).first()
        return table_data[0]

    def update_count_of_checks(self, user_id: int):
        count = self.conn.execute(select(self.table.count_of_checked).where(self.table.id == user_id)).first()[0]
        count += 1
        request = update(self.table).where(self.table.id == user_id).values(count_of_checked=count)
        self.commit(request)
