from sqlalchemy import create_engine
import datetime
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column

engine = create_engine("sqlite:///events.db")

class Base(DeclarativeBase):
    pass

Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

class Events(Base):
    __tablename__ = 'events'
    id: Mapped[int] = mapped_column('id', primary_key=True)
    title: Mapped[str] = mapped_column('title')
    date: Mapped[datetime.date] = mapped_column('date')
    description: Mapped[str] = mapped_column('description')
    people_amount: Mapped[int] = mapped_column('people_amount')
    people_max: Mapped[int] = mapped_column('people_max')
    start_time: Mapped[datetime.time] = mapped_column('time_start')
    end_time: Mapped[datetime.time] = mapped_column('time_end')


class Registarations(Base):
    __tablename__ = 'registrations'
    id: Mapped[int] = mapped_column('id', primary_key=True)
    event_id: Mapped[int] = mapped_column('event_id')
    user_id: Mapped[int] = mapped_column('user_id')
    time_slot_start: Mapped[datetime.time] = mapped_column('time_slot_start')
    time_slot_end: Mapped[datetime.time] = mapped_column('time_slot_end')

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column('id', primary_key=True)
    email: Mapped[str] = mapped_column('email')
    name: Mapped[str] = mapped_column('name')
    password: Mapped[str] = mapped_column('password')

#name #name@example.com #password123
