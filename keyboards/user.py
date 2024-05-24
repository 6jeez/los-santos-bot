from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def get_main_menu():
    kb = [[KeyboardButton(text="💖 Get Weather"), KeyboardButton(text="💸 Donate")]]

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


async def get_cancel_menu():
    kb = [[KeyboardButton(text="❌ Cancel")]]

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard
