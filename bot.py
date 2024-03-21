import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram import F, types, Router, Bot
from config.config import Config, load_config
from app.handlers import guide, order, user, rate, feedback, admin
from config.config import settings
from aiogram.fsm.storage.memory import MemoryStorage
from app.keyboards.set_menu import set_main_menu
from sqladmin import Admin, expose
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger(__name__)
logging.getLogger('aiogram.event').setLevel(logging.WARNING)


async def main():
    # Настройка журналирования для вывода информации о работе бота
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
        '%(lineno)d - %(name)s - %(message)s'
    )
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
        '%(lineno)d - %(name)s - %(message)s'
    )
    logging.basicConfig(
        level=logging.ERROR,
        format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
        '%(lineno)d - %(name)s - %(message)s'
    )
    logging.basicConfig(
        level=logging.CRITICAL,
        format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
        '%(lineno)d - %(name)s - %(message)s'
    )

    # Логгирование о начале работы бота
    logger.info("Запуск бота")

    # Загрузка конфигурации бота
    config: Config = load_config()
    # Инициализация объекта бота
    bot: Bot = Bot(token=settings.BOT_TOKEN)
    # Создание диспетчера для обработки входящих запросов
    storage = MemoryStorage()
    dp: Dispatcher = Dispatcher(storage=storage)
    # меню в боте
    await set_main_menu(bot)
    # admin = Admin(async_session_maker, base, engine)

    # Включаем маршрутизаторы
    dp.include_router(user.router)
    dp.include_router(rate.router)
    dp.include_router(feedback.router)
    dp.include_router(guide.router)
    dp.include_router(admin.router)
    dp.include_router(order.router)
    # уведомления для изменения курса юаня
    schelduler = AsyncIOScheduler(timezone="Europe/Moscow")
    schelduler.add_job(admin.notification, trigger='cron', hour=8, minute=0, second=0)
    schelduler.start()

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
