from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

import app.keyboards as kb


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать! 👋\n', reply_markup=kb.main)


@router.message(Command(commands='menu' or F.text.lower() == 'меню'))
async def cmd_menu(message: Message):
    pass


@router.message(Command(commands='plans' or F.text.lower() == 'список'))
async def cmd_plans(message: Message):
    pass


@router.message(Command(commands='new'))
async def cmd_new(message: Message):
    pass


@router.message(Command(commands='help' or F.text.lower() == 'помощь'))
async def cmd_help(message: Message):
    pass