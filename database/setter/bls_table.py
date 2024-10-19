from sqlalchemy import select
from database.creator import Bls
from database.setter.base_setter import DataBase


class BlsTable(DataBase):
    def __init__(self):
        super().__init__(Bls)

    def get_all_user_check(self, user_id: int):
        table_data = self.conn.execute(select(self.table).where(self.table.user_id == user_id)).all()
        return table_data
