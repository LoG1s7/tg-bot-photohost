from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.config import ADMIN_ID

menu_router = Router()


@menu_router.message(Command(commands=["menu"]))
async def show_menu(message: types.Message):
    """Отображение меню с командами пользователя."""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Добавить фото", callback_data="add_photo")
    if str(message.from_user.id) == ADMIN_ID:
        keyboard.button(
            text="Админ панель", callback_data="view_photos"
        )
    keyboard.button(text="Доступные команды", callback_data="help")
    await message.answer(
        "Выберите команду:", reply_markup=keyboard.as_markup()
    )


@menu_router.callback_query(lambda c: c.data == "add_photo")
async def handle_add_photo(callback_query: CallbackQuery):
    """Обработка нажатия на кнопку 'Добавить фото'."""
    await callback_query.answer()
    await callback_query.message.answer(
        "Выберите команду /add_photo для добавления фотографий."
    )


@menu_router.callback_query(lambda c: c.data == "view_photos")
async def handle_view_photos(callback_query: CallbackQuery):
    """Обработка нажатия на кнопку 'Просмотреть загруженные фото'."""
    await callback_query.answer()
    await callback_query.message.answer(
        "Выберите команду /view_users_photos "
        "для просмотра загруженных фотографий."
    )


@menu_router.callback_query(lambda c: c.data == "help")
async def handle_help(callback_query: CallbackQuery):
    """Обработка нажатия на кнопку 'Получить помощь'."""
    await callback_query.answer()
    await callback_query.message.answer(
        "/add_photo - загрузка фотографий \n"
        "/view_users_photos - просмотр загруженных фото."
    )
