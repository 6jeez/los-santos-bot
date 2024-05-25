from typing import Any

from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.user import get_cancel_menu, get_ban_menu
from states.ban_user import BanUser
from config import ADMIN_ID

router = Router()


@router.message(F.text == "💢 Ban/Unban")
async def ban_unban(msg: Message) -> Any:
    await msg.answer("Use menu below", reply_markup=await get_ban_menu())


@router.message(F.text == "🧡 Ban user")
async def start_ban_user(msg: Message, state: FSMContext, bot: Bot) -> Any:
    user_id = msg.from_user.id

    if user_id in ADMIN_ID:
        await msg.answer("write user id for ban", reply_markup=await get_cancel_menu())
        await state.set_state(BanUser.user_id)
