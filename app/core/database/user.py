import datetime

from sqlalchemy import Column, Integer, VARCHAR, DATE, BigInteger

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    user_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
    username = Column(VARCHAR(32), unique=False, nullable=True)
    reg_date = Column(DATE, default=datetime.date.today())


class Service(BaseModel):
    __tablename__ = "services"

    service_id = Column(Integer, autoincrement=False, primary_key=True)
    service = Column(VARCHAR(32), unique=False, nullable=True)
    months = Column(Integer, nullable=True)
    deadline = Column(DATE, nullable=True)
    reminder = Column(Integer, nullable=True)
