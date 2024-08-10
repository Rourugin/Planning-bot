import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from app.commands_menu import set_command
from app.database.models import async_main
from app.handlers import router


async def main() -> None:
    await async_main()
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    print("bot is working")
    dp.include_router(router=router)
    await set_command(bot=bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("bot was disabled")