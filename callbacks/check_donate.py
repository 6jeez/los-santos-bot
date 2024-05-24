from AsyncPayments.cryptoBot import AsyncCryptoBot

from typing import Any

from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery

from aiogram.fsm.context import FSMContext

from config import CRYPTO_BOT_TOKEN


router = Router()


@router.callback_query(F.data.startswith("paid_"))
async def get_paid_check(callback: CallbackQuery, bot: Bot, state: FSMContext) -> Any:
    user_id = callback.from_user.id
    invoice_id = callback.data.split("paid_")[-1]

    cryptoBot = AsyncCryptoBot(CRYPTO_BOT_TOKEN)

    info_crypto_bot = await cryptoBot.get_invoices(invoice_ids=invoice_id, count=1)
    invoice_status = info_crypto_bot[0].status

    if invoice_status == "paid":
        await bot.send_message(user_id, "💦 thx for the donation")
        await state.clear()
    else:
        await bot.send_message(user_id, "💥 you are not paid")
