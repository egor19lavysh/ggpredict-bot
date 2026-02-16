from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
from sqlalchemy import Integer


class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int]