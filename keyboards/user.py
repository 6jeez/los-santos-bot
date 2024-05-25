from typing import Any
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def get_main_menu(admin=None):
    if not admin:
        kb = [[KeyboardButton(text="💖 Get Weather"), KeyboardButton(text="💸 Donate")]]
    else:
        kb = [
            [KeyboardButton(text="💖 Get Weather"), KeyboardButton(text="💸 Donate")],
            [KeyboardButton(text="💢 Ban/Unban")],
            [KeyboardButton(text="📮 Newsletter")],
        ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


async def get_cancel_menu():
    kb = [[KeyboardButton(text="❌ Cancel")]]

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


async def get_ban_menu() -> Any:
    kb = [
        [KeyboardButton(text="🧡 Ban user")],
        [KeyboardButton(text="💙 Unban user")],
        [KeyboardButton(text="🔙 Main menu")],
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


async def get_media_menu() -> Any:
    kb = [
        [KeyboardButton(text="audio"), KeyboardButton(text="image")],
        [KeyboardButton(text="video"), KeyboardButton(text="document")],
        [KeyboardButton(text="nothing"), KeyboardButton(text="❌ Cancel")],
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard
