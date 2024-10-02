from datetime import datetime

from sqlalchemy import BigInteger, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base



class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]



class Tasks(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user: Mapped[str] = mapped_column(ForeignKey('users.login'))
    description: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())


