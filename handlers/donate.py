from typing import Any

from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.donate_state import DonateClass
from middlewares.throt import throttled
from middlewares.throt import ThrottlingMiddleware
from keyboards.user import get_cancel_menu

router = Router()
router.message.middleware(ThrottlingMiddleware())


@router.message(F.text == "💸 Donate")
@throttled(
    rate=5,
    on_throttle=lambda msg, data: msg.answer("🎃 Too many requests, please wait!"),
)
async def start_donate(msg: Message, bot: Bot, state: FSMContext) -> Any:
    user_id = msg.from_user.id

    await bot.delete_message(user_id, message_id=msg.message_id)
    donate_msg = await msg.answer(
        "😎 indicate the amount of the desired donation in USDT",
        reply_markup=await get_cancel_menu(),
    )

    await state.update_data({"donate_msg": donate_msg.message_id})
    await state.set_state(DonateClass.donate_sum)
