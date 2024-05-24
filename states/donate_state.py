from AsyncPayments.cryptoBot import AsyncCryptoBot

from typing import Any

from aiogram import Router, Bot, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.user import get_cancel_menu
from config import CRYPTO_BOT_TOKEN
from utils.numbers_checker import check_number


router = Router()


class DonateClass(StatesGroup):
    donate_sum = State()
    check = State()


@router.message(DonateClass.donate_sum)
async def get_donate_sum(msg: Message, bot: Bot, state: FSMContext) -> Any:
    user_id = msg.from_user.id
    sum = msg.text

    checked_num = check_number(sum)

    if not checked_num:
        await msg.answer("🤬 you didn't send a number")
        return

    data = await state.get_data()
    cryptoBot = AsyncCryptoBot(CRYPTO_BOT_TOKEN)

    order_crypto_bot = await cryptoBot.create_invoice(
        float(sum), currency_type="crypto", asset="USDT"
    )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❤ Pay", url=order_crypto_bot.pay_url)],
            [
                InlineKeyboardButton(
                    text="💚 I paid",
                    callback_data=f"paid_{order_crypto_bot.invoice_id}",
                )
            ],
        ]
    )

    await msg.answer("donate pay link", reply_markup=kb)
