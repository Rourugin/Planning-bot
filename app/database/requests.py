from sqlalchemy import select

from app.database.models import async_session
from app.database.models import User, ListOfTasks


async def set_user(user_name: str):
    async with async_session() as session:
        tg_user_name = await session.scalar(select(User).where(User.user_name == user_name))

        if not tg_user_name:
            session.add(User(user_name=user_name))
            await session.commit()