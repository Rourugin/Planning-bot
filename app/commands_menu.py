from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_command(bot: Bot):
    commands = [
        BotCommand(
            command='menu',
            description='Меню'
        ),
        BotCommand(
            command='plans',
            description='Список блоков задач'
        ),
        BotCommand(
            command='new',
            description='Создать новый блок задач'
        ),
        BotCommand(
            command='help',
            description='Помощь'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())