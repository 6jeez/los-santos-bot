import asyncio
from aiogram import Bot, Dispatcher

from database.database_funcs import Database
from config import TOKEN, DB_PATH, WEATHER_API_KEY
from handlers import user_commands, get_weather
from states import add_city
from services.weather_service import WeatherService


db = Database(db_name=DB_PATH)
weather_service = WeatherService(api_key=WEATHER_API_KEY)


async def main():
    await db.init()

    bot = Bot(TOKEN)
    dp = Dispatcher()

    dp.include_routers(user_commands.router, add_city.router, get_weather.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())