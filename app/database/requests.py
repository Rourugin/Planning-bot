from sqlalchemy import select

from app.database.models import async_session
from app.database.models import User, ListOfTasks


async def set_user(user_name: str):
    async with async_session() as session:
        tg_user_name = await session.scalar(select(User).where(User.user_name == user_name))

        if not tg_user_name:
            session.add(User(user_name=user_name))
            await session.commit()


async def check_nullable_lists():
    lists_tb_nl = '''
    SELECT True FROM lists LIMIT 1;
    '''

    return lists_tb_nl
