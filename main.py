import asyncio
import config
import db
from bot_init import bot, dp

from typing import Any
from aiogram.types import Update

from fastapi import FastAPI
from fastapi.requests import Request

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.initialize()
    await bot.delete_webhook()
    await bot.set_webhook(f'{config.webhook_url}/webhook')
    try:
        yield
    finally:
        await bot.delete_webhook()

app = FastAPI(lifespan=lifespan)

@app.get('/')
async def root():
    return {"message": "Hello World"}

@app.post('/webhook')
async def webhook(update: dict[str, Any]):
    await dp.feed_webhook_update(bot=bot, update=Update(**update))
    return {'status': 'ok'}
