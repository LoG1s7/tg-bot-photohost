import logging
import os

from aiogram import Bot, types

from bot.config import API_TOKEN, HOST, PORT, UPLOAD_FOLDER

bot = Bot(token=API_TOKEN)


async def save_photos(photo_id_list: list[str], user_id: int) -> None:
    """Сохранение фотографий."""
    for photo_id in photo_id_list:
        file_info = await bot.get_file(photo_id)
        file_name = f"{user_id}_{photo_id}.jpg"
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        await bot.download_file(file_info.file_path, destination=file_path)
        logging.info(f"Фотография {file_name} сохранена.")


async def notify_user_photos_uploaded(message: types.Message, user_id: int):
    """Уведомление о завершении загрузки всех фотографий."""
    await message.answer(
        "Все фотографии успешно загружены! Вот ваша ссылка:",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Просмотреть фотографии",
                        url=f"http://{HOST}:{PORT}/view_photos/{user_id}",
                    )
                ]
            ]
        ),
    )
