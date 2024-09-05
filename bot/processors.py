from aiogram import Bot, F, Router, types
from aiogram.fsm.context import FSMContext

from bot.config import API_TOKEN
from bot.states import Photo
from bot.utils import notify_user_photos_uploaded, save_photos

list_photo = {}

bot = Bot(token=API_TOKEN)

processors_router = Router()


@processors_router.message(Photo.count)
async def process_photo_count(message: types.Message, state: FSMContext):
    """Обработка количества фотографий."""
    try:
        count = int(message.text)
        if count > 10:
            await message.answer(
                text="Вы можете загрузить за раз не более 10 фото.",
            )
            await state.clear()
        elif count < 1:
            await message.answer(
                text="Количество фото должно быть больше 0. \n"
                "Для добавления фотографий напишите '/add_photo'.",
            )
            await state.clear()
        else:
            await state.update_data(photo_count=count)
            await state.set_state(Photo.photo_id)
            await message.answer(
                "Пожалуйста, загрузите ваши фотографии одним сообщением. \n"
                "Для отмены загрузки напишите '/cancel'."
            )
    except TypeError:
        await message.answer(
            "Перед отправкой фото введите число. \n"
            "Для отмены загрузки напишите '/cancel'."
        )
    except ValueError:
        await message.answer(
            "Введите корректное число. \n"
            "Для отмены загрузки напишите '/cancel'."
        )


@processors_router.message(Photo.photo_id, F.photo)
async def get_photo(message: types.Message, state: FSMContext):
    """Получение фотографий и сохранение на сервере."""
    global list_photo
    data = await state.get_data()
    user_id = message.from_user.id
    list_photo.setdefault(str(user_id), [])
    if message.content_type == "photo":
        list_photo[str(user_id)].append(message.photo[-1].file_id)
        if len(list_photo[str(user_id)]) == int(data.get("photo_count")):
            await save_photos(list_photo[str(message.chat.id)], user_id)
            await notify_user_photos_uploaded(message, user_id)
            await state.clear()
            list_photo = {}
