from typing import Any
from aiogram import Router, Bot, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from config import ADMIN_ID

router = Router()


@router.message(F.text == "💙 Unban user")
async def start_unban_users(msg: Message) -> Any:
    from main import db

    user_id = msg.from_user.id

    if user_id in ADMIN_ID:
        users = await db.get_all_user_ids()

        buttons = []

        for user in users:
            buttons.append(
                [InlineKeyboardButton(text=f"{user}", callback_data=f"unban_{user}")]
            )

        kb = InlineKeyboardMarkup(inline_keyboard=buttons)

        await msg.answer("Chose user id for unban", reply_markup=kb)


@router.callback_query(F.data.startswith("unban_"))
async def end_unban_user(callback: CallbackQuery, bot: Bot) -> Any:
    from main import db

    user_id = callback.data.split("unban_")[-1]
    await db.unban_user(user_id)

    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        text=f"<b>You successfully unbanned user:</b> <code>{user_id}</code>",
        message_id=callback.message.message_id,
        reply_markup=None,
        parse_mode="HTML",
    )
