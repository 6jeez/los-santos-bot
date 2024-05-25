from typing import Any

from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types.input_file import FSInputFile

from keyboards.user import get_cancel_menu, get_media_menu, get_main_menu
from config import ADMIN_ID
from utils.folders import delete_media

router = Router()


class Newsletter(StatesGroup):
    message_text = State()
    media = State()
    download_media = State()


@router.message(F.text == "📮 Newsletter")
async def start_newsletter(msg: Message, state: FSMContext) -> Any:
    user_id = msg.from_user.id

    if user_id in ADMIN_ID:
        await msg.answer(
            text="Write text for newsletter", reply_markup=await get_cancel_menu()
        )
        await state.set_state(Newsletter.message_text)


@router.message(Newsletter.message_text)
async def get_message_text(msg: Message, state: FSMContext) -> Any:
    user_id = msg.from_user.id

    if msg.text:
        await state.update_data({"messsage_text": msg.text})

        await msg.answer(
            "Chose what media you want pin", reply_markup=await get_media_menu()
        )
        await state.set_state(Newsletter.media)


@router.message(Newsletter.media)
async def get_media(msg: Message, state: FSMContext, bot: Bot) -> Any:
    answer = msg.text.lower()

    if answer in ["audio", "image", "video", "document", "nothing"]:
        await state.update_data({"media_type": answer})

        await msg.answer("Send media for me", reply_markup=await get_cancel_menu())
        await state.set_state(Newsletter.download_media)


@router.message(Newsletter.download_media)
async def get_media(msg: Message, state: FSMContext, bot: Bot) -> Any:
    from main import db

    data = await state.get_data()
    newsletter_text = data.get("messsage_text")
    media_type = data.get("media_type")
    users = await db.get_all_user_ids()
    success = 0
    failed = 0

    if msg.document and media_type == "document":
        file_id = msg.document.file_id

        File = await bot.get_file(file_id)
        print(File)

        file = await bot.get_file(file_id)
        file_path = file.file_path
        file_name = file_path.split("/")[-1]

        await bot.download_file(file_path, f"media/{file_name}")

        for user in users:
            file = FSInputFile(path=f"media/{file_name}")
            try:
                await bot.send_document(user, file, caption=newsletter_text)
                success += 1
            except:
                failed += 1

    elif msg.audio and media_type == "audio":
        file_id = msg.audio.file_id

        File = await bot.get_file(file_id)
        print(File)

        file = await bot.get_file(file_id)
        file_path = file.file_path
        file_name = file_path.split("/")[-1]

        await bot.download_file(file_path, f"media/{file_name}")

        for user in users:
            file = FSInputFile(path=f"media/{file_name}")
            try:
                await bot.send_audio(user, file, caption=newsletter_text)
                success += 1
            except:
                failed += 1

    elif msg.photo and media_type == "image":
        file_id = msg.photo[-1].file_id

        File = await bot.get_file(file_id)
        print(File)

        file = await bot.get_file(file_id)
        file_path = file.file_path

        file_name = file_path.split("/")[-1]

        await bot.download_file(file_path, f"media/{file_name}")

        for user in users:
            file = FSInputFile(path=f"media/{file_name}")
            try:
                await bot.send_photo(user, file, caption=newsletter_text)
                success += 1
            except:
                failed += 1

    elif msg.video and media_type == "video":
        file_id = msg.video.file_id

        File = await bot.get_file(file_id)
        print(File)

        file = await bot.get_file(file_id)
        file_path = file.file_path
        file_name = file_path.split("/")[-1]

        await bot.download_file(file_path, f"media/{file_name}")

        for user in users:
            file = FSInputFile(path=f"media/{file_name}")
            try:
                await bot.send_video(user, file, caption=newsletter_text)
                success += 1
            except:
                failed += 1

    elif msg.text:
        for user in users:
            try:
                await bot.send_message(user, newsletter_text)
                success += 1
            except:
                failed += 1

    await state.clear()

    delete_media()

    await msg.answer(
        f"<b>Stat:</b>\nSuccess: <code>{success}</code>\nFailed: <code>{failed}</code>",
        parse_mode="HTML",
        reply_markup=await get_main_menu(admin=True),
    )
