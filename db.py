import asyncpg
import config
import asyncio
import database

users = database.users()
videos = database.videos()
free_videos = database.free_videos()
payments = database.payments()
tests = database.tests()

async def initialize():
    db = await asyncpg.create_pool(config.db_url)

    users.connect(db)
    await users.create_table()

    videos.connect(db)
    await videos.create_table()

    free_videos.connect(db)
    await free_videos.create_table()

    payments.connect(db)
    await payments.create_table()

    tests.connect(db)
    await tests.create_table()

if __name__ == '__main__':
    asyncio.run(initialize())