from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

import app.states as st
import app.keyboards as kb
import app.database.requests as rq


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать! 👋\nЗдесь вы можете создать себе планы, отслеживать изменения и управлять ими!', reply_markup=kb.main)
    await rq.set_user(message.from_user.username)


@router.message(Command(commands='menu' or F.text.lower() == 'меню'))
async def cmd_menu(message: Message):
    await message.answer('Отсюда Вы можете отправиться в любую точку бота!', reply_markup=kb.main)


@router.message(Command(commands='plans' or F.text.lower() == 'список'))
async def cmd_plans(message: Message):
    pass


@router.message(Command(commands='new_list'))
async def cmd_new(message: Message):
    pass


@router.message(Command(commands='new_task'))
async def cmd_new(message: Message):
    pass


@router.message(Command(commands='help' or F.text.lower() == 'помощь'))
async def cmd_help(message: Message):
    await message.answer('Если Вы не можете попасть в какой-либо раздел, попробуйте воспользоваться меню.\n' + 
                         'Если проблемы всё ещё остались, Вы можете обратиться к @Rouruginn')