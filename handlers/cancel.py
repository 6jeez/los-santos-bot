from typing import Any

from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.donate_state import DonateClass
from middlewares.throt import throttled
from middlewares.throt import ThrottlingMiddleware
from keyboards.user import get_main_menu

router = Router()


@router.message(F.text == "❌ Cancel")
async def cancel_states(msg: Message, state: FSMContext) -> Any:
    await state.clear()

    await msg.answer(
        text="💢 you canceled the action", reply_markup=await get_main_menu()
    )
