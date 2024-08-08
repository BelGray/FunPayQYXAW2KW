import asyncio

import sqlalchemy as db
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import database.db_config as tables
from aiogram import types, F
from aiogram.filters import Command, StateFilter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile

from admin import Admin
from daily_image_manager import DailyImage
from database.db_config import conn
from loader import dp, bot, tribute
from tools import user_register


class FileImg(StatesGroup):
    img = State()


@dp.message(Command("start"))
async def start(message: types.Message):
    await user_register(message)
    start_text = "Ты настоящий sigma, если зашел в нашего бота!"
    buttons = [[InlineKeyboardButton(text="Выдать доступ на 24 часа", callback_data="av_24")],
               [InlineKeyboardButton(text="Купить доступ на месяц", url=tribute)]]
    if await Admin.is_admin(message.from_user.id):
        buttons.append(
            [InlineKeyboardButton(text="Загрузить фотографию [только админ]", callback_data="upload_photo")]
        )
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.send_message(message.chat.id, start_text, reply_markup=markup)


@dp.callback_query(F.data == 'av_24')
async def av_24_callback(callback: types.CallbackQuery):
    await user_register(callback)
    user_query = conn.execute(
        db.select(tables.users).where(tables.users.columns.telegram_id.like(callback.from_user.id))
    )
    user = user_query.fetchall()
    if user[0][1] is True:
        await callback.answer("Ты уже ранее получал(-а) доступ на 24 часа", show_alert=True)
        return
    path = await DailyImage.get_path()
    if path is None:
        await callback.answer("Невозможно на данный момент получить доступ (администратор не загрузил данные).",
                              show_alert=True)
        return
    if not await DailyImage.exists(path):
        await callback.answer("Невозможно на данный момент получить доступ (администратор не загрузил данные).",
                              show_alert=True)
        return
    await bot.send_photo(chat_id=callback.message.chat.id, photo=FSInputFile(path))
    conn.execute(
            db.update(tables.users).where(
                tables.users.columns.telegram_id == callback.from_user.id
            ).values(
                used=True
            )
        )
    conn.commit()


@dp.callback_query(StateFilter(None), F.data == "upload_photo")
async def upload_photo(callback: types.CallbackQuery, state: FSMContext):
    await user_register(callback)
    if not await Admin.is_admin(callback.from_user.id):
        await callback.answer("Ты не можешь воспользоваться данной опцией, так как ты не администратор",
                              show_alert=True)
        return
    await bot.send_message(chat_id=callback.message.chat.id, text="Отправь фотографию, которая будет видна тем пользователям, кто нажал кнопку 'Получить доступ на 24 часа'.")
    await state.set_state(FileImg.img)


@dp.message(FileImg.img, F.content_type == ContentType.PHOTO)
async def file_image_input(message: types.Message, state: FSMContext):
    if not await Admin.is_admin(message.from_user.id):
        return
    await state.clear()
    try:
        file_id = message.photo[0].file_id
        file_path = await bot.get_file(file_id)
        await DailyImage.remove_current_path()
        await DailyImage.save(file_path)
        await bot.send_message(chat_id=message.chat.id, text="Изображение сохранено успешно")
    except Exception as e:
        return await bot.send_message(chat_id=message.chat.id,
                                      text=f"Что-то пошло не так при получении и сохранении изображения.\n<code>{e}</code>")


async def on_ready():
    await DailyImage.init_json()
    print(await bot.me())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(on_ready())
