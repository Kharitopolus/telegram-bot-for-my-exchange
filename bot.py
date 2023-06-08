import asyncio
from aiogram import Bot, Dispatcher
from config_data.config import load_tg_bot_config, TgBot
from handlers import (
    login,
    take_order,
    quote,
    del_messsage,
    cancel_form,
    unforeseen_action,
)
from keyboards.main_menu import set_main_menu


async def main():
    config: TgBot = load_tg_bot_config()
    bot: Bot = Bot(token=config.token)
    dp: Dispatcher = Dispatcher()
    await set_main_menu(bot)
    dp.include_router(del_messsage.router)
    dp.include_router(quote.router)
    dp.include_router(cancel_form.router)
    dp.include_router(login.router)
    dp.include_router(take_order.router)
    dp.include_router(unforeseen_action.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
