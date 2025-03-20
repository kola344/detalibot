from aiogram import Bot, Dispatcher
import config

from bot.admin.messages import router as mainAdminRouter
from bot.admin.freeVideos.messages import router as freeVideosAdminRouter
from bot.admin.videos.messages import router as videosAdminRouter
from bot.admin.tests.messages import router as testsAdminRouter
from bot.admin.dbtools.messages import router as dbtoolsAdminRouter
from bot.admin.broadcasts.messages import router as broadcastsAdminRouter

from bot.user.messages import router as mainUserRouter

bot = Bot(config.bot_token)
dp = Dispatcher()

dp.include_router(mainAdminRouter)
dp.include_router(freeVideosAdminRouter)
dp.include_router(videosAdminRouter)
dp.include_router(testsAdminRouter)
dp.include_router(dbtoolsAdminRouter)
dp.include_router(broadcastsAdminRouter)

dp.include_router(mainUserRouter)