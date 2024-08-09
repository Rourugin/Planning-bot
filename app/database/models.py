import os
from typing import Optional
from time import struct_time
from dotenv import load_dotenv
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


load_dotenv()
engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'))
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str]


class ListOfTasks(Base):
    __tablename__ = 'lists'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[BigInteger]
    name: Mapped[str]
    description: Mapped[Optional[str]]
    condition: Mapped[Optional[int]]


class task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[BigInteger]
    name: Mapped[str]
    parent_list: Mapped[str] = mapped_column(ForeignKey("lists.id"))
    description: Mapped[Optional[str]]
    time_to_comlete: Mapped[Optional[struct_time]]
    condition: Mapped[Optional[int]]


async def async_main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)