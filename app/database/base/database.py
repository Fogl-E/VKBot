from sqlalchemy import BigInteger, DateTime, String, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True) 
    recording: Mapped[str] = mapped_column(String(100), default="не записан")


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    time_slot: Mapped[datetime.datetime] = mapped_column(DateTime)