from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='📝 Список'),
     KeyboardButton(text='⚠ Важные')],
    [KeyboardButton(text='▶ В процессе'),
     KeyboardButton(text='💡 Все дела')],
    [KeyboardButton(text='⚙ Помощь')]
], resize_keyboard=True)