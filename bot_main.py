import asyncio
import logging
import os
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.commands import commands_router
from bot.config import API_TOKEN, UPLOAD_FOLDER
from bot.menu import menu_router
from bot.processors import processors_router


def cleanup_photos():
    """Удаление старых фотографий."""
    now = datetime.now()
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
            if now - creation_time > timedelta(days=30):
                os.remove(file_path)


async def run_bot():
    """Запуск бота и очистка старых фотографий."""
    cleanup_photos()
    bot = Bot(token=API_TOKEN)
    logging.basicConfig(level=logging.INFO)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(processors_router)
    dp.include_router(commands_router)
    dp.include_router(menu_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_bot())
