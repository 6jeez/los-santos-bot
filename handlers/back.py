from typing import Any

from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.methods.get_chat import GetChat

from keyboards.user import get_main_menu

from config import ADMIN_ID

router = Router()


@router.message(F.text == "🔙 Main menu")
async def cancel_states(msg: Message, state: FSMContext, bot: Bot) -> Any:
    user_id = msg.from_user.id
    admin = True if user_id in ADMIN_ID else None
    await state.clear()

    await msg.answer(
        text="🔙 you in main menu", reply_markup=await get_main_menu(admin)
    )
