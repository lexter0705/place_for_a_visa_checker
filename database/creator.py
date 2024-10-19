from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Boolean
import json_checker

DATABASE_URL = "sqlite:///" + json_checker.get_data_for_parser()["data_base_path"]
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    count_of_checked = Column(Integer)
    is_height_priority = Column(Boolean)


class Bls(Base):
    __tablename__ = 'bots'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    email = Column(String)
    pass_account = Column(String)
    jurisdiction = Column(String)
    location = Column(String)
    visa_type = Column(String)
    visa_sub_type = Column(String)
    appointment_category = Column(String)
    proxy_ip_port = Column(String)
    proxy_login = Column(String)
    proxy_password = Column(String)


def create():
    Base.metadata.create_all(bind=engine)
    print("Database Created!")


if __name__ == "__main__":
    create()
