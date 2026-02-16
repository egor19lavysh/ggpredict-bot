from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
from sqlalchemy import Integer



class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str]