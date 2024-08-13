import os
from dotenv import load_dotenv
from sqlalchemy import ForeignKey
from typing import Optional, Annotated
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


load_dotenv()
engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'))
async_session = async_sessionmaker(engine)
intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    user_name: Mapped[str]


class ListOfTasks(Base):
    __tablename__ = 'lists'

    id: Mapped[intpk]
    name: Mapped[str]
    user_id: Mapped[int]
    description: Mapped[Optional[str]]
    importance: Mapped[int]
    condition: Mapped[Optional[int]]


class task(Base):
    __tablename__ = 'tasks'

    id: Mapped[intpk]
    name: Mapped[str]
    user_id: Mapped[int]
    parent_list: Mapped[str] = mapped_column(ForeignKey("lists.id"))
    description: Mapped[Optional[str]]
    time_to_comlete: Mapped[Optional[int]]
    importance: Mapped[int]
    condition: Mapped[Optional[int]]


async def async_main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)