from sqlalchemy import Column, VARCHAR, DATE, BIGINT, INT

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    user_id = Column(BIGINT, unique=True, nullable=False, primary_key=True)
    username = Column(VARCHAR(32), unique=False, nullable=True)


class Service(BaseModel):
    __tablename__ = "services"

    service_id = Column(INT, autoincrement=False, primary_key=True)
    service = Column(VARCHAR(32), unique=False, nullable=True)
    months = Column(INT, nullable=True)
    deadline = Column(DATE, nullable=True)
    reminder = Column(INT, nullable=True)
