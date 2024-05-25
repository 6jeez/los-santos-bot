from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.user import get_main_menu

router = Router()


class BanUser(StatesGroup):
    user_id = State()


@router.message(BanUser.user_id)
async def end_ban_user(msg: Message, state: FSMContext, bot: Bot):
    from main import db

    try:
        user_id = int(msg.text)
        user = await db.get_user(user_id)
    except Exception as ex:
        print(f"[ERROR] {ex}")
        user = None

    if user is None:
        await msg.answer(text=f"There is no such user in the database")
        return

    await db.ban_user(user_id)
    await msg.answer(
        text=f"You successfully banned user: {user_id}",
        reply_markup=await get_main_menu(admin=True),
    )
    await state.clear()
