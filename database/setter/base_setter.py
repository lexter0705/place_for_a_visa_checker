from sqlalchemy import create_engine
from sqlalchemy import insert, select, delete, update
import json_checker


class DataBase:
    def __init__(self, table):
        self.DATABASE_URL = "sqlite:///" + json_checker.get_data_for_parser()["data_base_path"]
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
