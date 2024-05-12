from sqlalchemy import create_engine
from sqlalchemy import insert, select, delete, update
from database.creator import Users, Bls
import json_checker


class DataBase:

    def __init__(self, table):
        self.DATABASE_URL = "sqlite:///" + json_checker.get_data_for_web_bot()["data_base_path"]
        self.engine = create_engine(self.DATABASE_URL)
        self.conn = self.engine.connect()
        self.table = table

    def add_to_database(self, data: dict):
        request = insert(self.table).values(**data)
        self.commit(request)

    def delete_from_database(self, user_id: int):
        request = delete(self.table).where(self.table.id == f"{user_id}")
        self.commit(request)

    def update_database(self, user_id: int, user_data: dict):
        request = update(self.table).where(self.table.id == f"{user_id}").values(**user_data)
        self.commit(request)

    def select_all_from_database(self):
        table_data = self.conn.execute(select(self.table)).all()
        return table_data

    def get_columns_name(self):
        columns = self.conn.execute(select(self.table)).columns()
        return columns

    def commit(self, request):
        self.conn.execute(request)
        self.conn.commit()


class UserTable(DataBase):
    def __init__(self):
        super().__init__(Users)

    def get_users_with_high_priority(self):
        table_data = self.conn.execute(select(self.table).where(self.table.is_height_priority is True)).all()
        return table_data

    def get_users_with_low_priority(self):
        table_data = self.conn.execute(select(self.table).where(self.table.is_height_priority is False)).all()
        return table_data


class BlsTable(DataBase):
    def __init__(self):
        super().__init__(Bls)

    def get_all_user_check(self, user_id: int):
        table_data = self.conn.execute(select(self.table).where(self.table.user_id == user_id)).all()
        return table_data
