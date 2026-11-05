from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column

engine = create_engine("sqlite:///event.db")

class Base(DeclarativeBase):
    pass

Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

class Events(Base):
    __tablename__ = 'events'
    id: Mapped[int] = mapped_column('id', primary_key=True)
    title: Mapped[str] = mapped_column('title')
    date: Mapped[str] = mapped_column('date')
    description: Mapped[str] = mapped_column('description')
    people_amount: Mapped[int] = mapped_column('people_amount')
    people_max: Mapped[int] = mapped_column('people_max')


class Registarations(Base):
    __tablename__ = 'registrations'
    id: Mapped[int] = mapped_column('id', primary_key=True)
    event_id: Mapped[int] = mapped_column('event_id')
    user_id: Mapped[int] = mapped_column('user_id')

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column('id', primary_key=True)
    email: Mapped[str] = mapped_column('email')
    username: Mapped[str] = mapped_column('username')
    password: Mapped[str] = mapped_column('password')
