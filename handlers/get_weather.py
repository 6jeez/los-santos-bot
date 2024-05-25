from typing import Any

from aiogram import Router, F, Bot
from aiogram.types import Message
from middlewares.throt import throttled
from middlewares.throt import ThrottlingMiddleware


router = Router()
router.message.middleware(ThrottlingMiddleware())


@router.message(F.text == "💖 Get Weather")
@throttled(
    rate=5,
    on_throttle=lambda msg, data: msg.answer("🎃 Too many requests, please wait!"),
)
async def get_user_weather(msg: Message, bot: Bot) -> Any:
    from main import db, weather_service

    user_id = msg.from_user.id

    user = await db.get_user(user_id=user_id)
    if user.get("is_ban") == "yes":
        return

    user_data = await db.get_user(user_id=user_id)
    user_city = user_data.get("city")

    user_weather = await weather_service.get_weather(city_name=user_city)

    if user_weather:
        msg_text = ""

        msg_text += f"🎈 <b>Current weather in {user_city}:</b>\n\n"
        msg_text += f"🥼 <i>Temperature: {user_weather['temperature']}°C</i>\n"
        msg_text += f"👖 <i>Description: {user_weather['description']}</i>"

        await msg.answer(msg_text, parse_mode="HTML")
