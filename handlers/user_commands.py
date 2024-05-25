from typing import Any

from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.user import get_main_menu
from states.add_city import AddCity
from main import db
from middlewares.throt import throttled
from middlewares.throt import ThrottlingMiddleware
from config import ADMIN_ID

router = Router()
router.message.middleware(ThrottlingMiddleware())


@router.message(F.text == "/start")
@throttled(
    rate=5,
    on_throttle=lambda msg, data: msg.answer("🎃 Too many requests, please wait!"),
)
async def start_func(msg: Message, bot: Bot, state: FSMContext) -> Any:
    user_id = msg.from_user.id
    admin = True if user_id in ADMIN_ID else None
    user = await db.get_user(user_id=user_id)

    if user.get("is_ban") == "yes":
        return

    await bot.delete_message(chat_id=user_id, message_id=msg.message_id)

    if not user:
        start_msg = await msg.answer(
            text=f"😘 Hi, <b>{msg.from_user.full_name}</b>.\n🌆 Enter your city name, for example: Washington",
            parse_mode="HTML",
        )
        await state.update_data({"start_msg": start_msg.message_id})
        await state.set_state(AddCity.name)

        return

    await msg.answer(
        text=f"😘 Hi, <b>{msg.from_user.full_name}</b>.\n🤞 Use menu below",
        parse_mode="HTML",
        reply_markup=await get_main_menu(admin),
    )
