import asyncio

import db
from bot_init import bot, dp

import asyncpg

async def main():
    await db.initialize()
    print('running')
    await dp.start_polling(bot)

asyncio.run(main())