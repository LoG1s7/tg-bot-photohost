from aiogram import Bot, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.config import ADMIN_ID, API_TOKEN, HOST, PORT
from bot.states import Photo

bot = Bot(token=API_TOKEN)

approved_users = set()
approved_users.add(int(ADMIN_ID))
commands_router = Router()


@commands_router.message(Command(commands=["start"]))
async def send_welcome(message: types.Message):
    """Команда /start."""
    if message.from_user.id not in approved_users:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(
            text="Подтвердить", callback_data=f"confirm:{message.from_user.id}"
        )
        await bot.send_message(
            ADMIN_ID,
            f"Пользователь {message.from_user.full_name} "
            f"хочет начать использовать бота.",
            reply_markup=keyboard.as_markup(),
        )
        await message.answer(
            "Ваш запрос отправлен админу. Ожидайте подтверждения."
        )
    else:
        await message.answer(
            "Добро пожаловать! Вы уже подтверждены. \n"
            " Используйте команду '/menu' "
            "для отображения меню с командами пользователя."
        )


@commands_router.callback_query(lambda c: c.data.startswith("confirm"))
async def process_callback_confirm(callback_query: CallbackQuery):
    """Подтверждение пользователя админом."""
    user_id = int(callback_query.data.split(":")[1])
    approved_users.add(user_id)
    await bot.send_message(
        user_id,
        "Ваш запрос был одобрен! Теперь вы можете использовать бота. \n"
        "Используйте команду '/menu' "
        "для отображения меню с командами пользователя.",
    )
    await callback_query.message.edit_text(
        f"Пользователь {user_id} был подтвержден!"
    )


@commands_router.message(Command(commands=["add_photo"]))
async def cmd_add_photo(message: types.Message, state: FSMContext):
    """Команда для добавления фотографий."""
    if message.from_user.id not in approved_users:
        await message.answer(
            "Вы еще не подтверждены. Ожидайте подтверждения администратора."
        )
    else:
        await state.set_state(Photo.count)
        await message.answer("Сколько фотографий вы хотите добавить?")


@commands_router.message(Command("cancel"))
async def cancel_upload(message: types.Message, state: FSMContext):
    """Отмена загрузки фотографий."""
    await state.clear()
    await message.answer("Загрузка фотографий отменена.")


@commands_router.message(Command(commands=["view_users_photos"]))
async def cmd_view_users_photos(message: types.Message):
    """Команда для просмотра фотографий пользователей в вебе."""
    if str(message.from_user.id) != ADMIN_ID:
        await message.answer("Эта команда доступна только администратору.")
        return

    flask_url = f"http://{HOST}:{PORT}/photos"
    await message.answer(
        "Админ панель с фото пользователей:",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Просмотреть фотографии",
                        url=flask_url,
                    )
                ]
            ]
        ),
    )
