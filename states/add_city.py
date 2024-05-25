from typing import Any

from aiogram import Router, Bot
from aiogram.types import Message

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from main import db, weather_service
from keyboards.user import get_main_menu
from config import ADMIN_ID


router = Router()


class AddCity(StatesGroup):
    name = State()


@router.message(AddCity.name)
async def get_city_name(msg: Message, bot: Bot, state: FSMContext) -> Any:
    user_id = msg.from_user.id
    data = await state.get_data()
    admin = True if user_id in ADMIN_ID else None

    is_city_exist = await weather_service.city_exists(city_name=msg.text)

    if not is_city_exist:
        await msg.answer(
            text="🤬 <b>There is no such city\n😠 Please, enter the correct city name</b>",
            parse_mode="HTML",
        )
        return

    await db.add_user(user_id=user_id, city=msg.text)

    await bot.delete_message(chat_id=user_id, message_id=msg.message_id)
    await bot.delete_message(chat_id=user_id, message_id=data.get("start_msg"))
    await msg.answer(
        text=f"✔ <b>You successfully added {msg.text} city!</b>\n\n😊Use menu below",
        reply_markup=await get_main_menu(admin),
        parse_mode="HTML",
    )

    await state.clear()
