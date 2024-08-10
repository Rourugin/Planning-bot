from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_command(bot: Bot):
    commands = [
        BotCommand(
            command='menu',
            description='Main menu'
        ),
        BotCommand(
            command='plans',
            description='List of your plans blocks'
        ),
        BotCommand(
            command='new_list',
            description='Create new plan list'
        ),
        BotCommand(
            command='new_task',
            description='Create new task'
        ),
        BotCommand(
            command='help',
            description='Help'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())