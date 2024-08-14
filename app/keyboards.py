from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='📝 Your plans'),
     KeyboardButton(text='⚠ Important')],
    [KeyboardButton(text='▶ In Progress'),
     KeyboardButton(text='⚙ Help')]
], resize_keyboard=True)


new_list_creation = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Quit", callback_data='menu'),
     InlineKeyboardButton(text="Create!", callback_data='creare_new_list')]
])


new_task_creation = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Let's get it!", callback_data='creare_new_task')],
    [InlineKeyboardButton(text="Quit", callback_data='menu')]
])