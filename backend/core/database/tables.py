from sqlalchemy import BIGINT, INT, VARCHAR, Column

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    user_id = Column(BIGINT, unique=True, nullable=False, primary_key=True)
    user_name = Column(VARCHAR(32), unique=False, nullable=True)


class Service(BaseModel):
    __tablename__ = "services"

    service_id = Column(INT, autoincrement=True, primary_key=True)
    service = Column(VARCHAR(32), unique=False, nullable=True)
    months = Column(INT, nullable=True)
    deadline = Column(VARCHAR(12), nullable=True)
    reminder = Column(INT, nullable=True)
