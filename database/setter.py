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

    def delete_from_database(self, some_id: int):
        request = delete(self.table).where(self.table.id == f"{some_id}")
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

    def select_user(self, user_id: int):
        table_data = self.conn.execute(select(self.table).where(self.table.id == user_id)).first()
        return table_data

    def get_user_count_checks(self, user_id: int):
        table_data = self.conn.execute(select(self.table.count_of_checked).where(self.table.id == user_id)).first()
        return table_data[0]

    def update_count_of_checks(self, user_id: int):
        count = self.conn.execute(select(self.table.count_of_checked).where(self.table.id == user_id)).first()[0]
        count += 1
        request = update(self.table).where(self.table.id == user_id).values(count_of_checked = count)
        self.commit(request)
        print(self.conn.execute(select(self.table.count_of_checked).where(self.table.id == user_id)).first()[0])


class BlsTable(DataBase):
    def __init__(self):
        super().__init__(Bls)

    def get_all_user_check(self, user_id: int):
        table_data = self.conn.execute(select(self.table).where(self.table.user_id == user_id)).all()
        return table_data
