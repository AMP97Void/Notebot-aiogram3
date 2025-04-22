import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.StateMachine import router1
from app.database.models import async_main 



async def main():
    await async_main()
    bot = Bot(token = 'TOKEN')
    dp = Dispatcher() #Класс, который обрабатывает сообщения
    
    dp.include_routers(router,router1)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
        


if __name__ == "__main__":  
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')