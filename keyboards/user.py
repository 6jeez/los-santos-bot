from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def get_main_menu():
    kb = [[KeyboardButton(text="💖 Get Weather"), KeyboardButton(text="💸 Donate")]]

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard
