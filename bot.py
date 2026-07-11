import os
import asyncio
import logging

from dotenv import load_dotenv

load_dotenv()

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

from search import search_similar

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# ---------------- START ----------------

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет 👋\n\nПришли фото товара, и я найду похожие товары 🔎"
    )


# ---------------- PHOTO ----------------

@dp.message(F.photo)
async def handle_photo(message: types.Message):

    file_path = None

    try:
        file = await bot.get_file(message.photo[-1].file_id)

        file_path = f"temp_{message.photo[-1].file_id}.jpg"

        await bot.download_file(file.file_path, file_path)

        results = search_similar(file_path, top_k=10)

        if not results:
            await message.answer("Ничего не найдено ❌")
            return

        text = "🔎 Найденные товары:\n\n"

        for i, r in enumerate(results, 1):

            text += (
                f"{i}. {r['text']}\n"
                f"🔗 {r['url']}\n"
                f"📊 score: {round(r['score'],3)}\n\n"
            )

        await message.answer(text)

    except Exception:

        logger.exception("Ошибка при обработке фотографии")

        await message.answer(
            "Произошла ошибка при поиске.\nПопробуйте ещё раз."
        )

    finally:

        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                logger.exception("Не удалось удалить временный файл")


# ---------------- MAIN ----------------

async def main():

    while True:

        try:

            logger.info("Бот запущен")

            await dp.start_polling(bot)

        except Exception:

            logger.exception("Polling завершился с ошибкой")

            logger.info("Повторный запуск через 10 секунд...")

            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
