import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.handlers import router


async def main() -> None:
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    print("бот запущен")
    dp.include_router(router=router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("бот был отключён")