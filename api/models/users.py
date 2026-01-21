from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column
from config.database import Base


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String, index=True, nullable=False, unique=True)
    password = mapped_column(String, nullable=False)
