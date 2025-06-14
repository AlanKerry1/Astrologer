import asyncio
from aiogram import Bot, Dispatcher
from handlers import router
import config

async def on_startup():
    print("БОТ ЗАПУЩЕН")

async def main():
    bot = Bot(config.TOKEN_BOT)
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.include_router(router)
    try:
        await dp.start_polling(bot, skip_updates=True, on_startup=on_startup)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
