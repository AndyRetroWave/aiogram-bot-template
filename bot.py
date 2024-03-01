import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import Config, load_config
from src.handlers import user, rate
from config.config import settings


logger = logging.getLogger(__name__)


async def main():
    # Настройка журналирования для вывода информации о работе бота
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    # Логгирование о начале работы бота
    logger.info("Запуск бота")

    # Загрузка конфигурации бота
    config: Config = load_config()

    # Инициализация объекта бота
    bot: Bot = Bot(token=settings.BOT_TOKEN)
    # Создание диспетчера для обработки входящих запросов
    dp: Dispatcher = Dispatcher()

    # Включаем маршрутизаторы
    dp.include_router(user.router)
    dp.include_router(rate.router)

    # Удаление вебхука и запуск бота с использованием лонг-поллинга
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        # Запуск основной функции бота
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # Обработка событий выхода из программы
        logger.info("Bot stopped")
