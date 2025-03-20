import db
import config
from bot.admin.broadcasts.replics import *
from bot.admin.broadcasts import keyboards
from bot.admin import models

from aiogram import Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import F
from aiogram.exceptions import TelegramBadRequest

from aiogram.fsm.context import FSMContext

from functions import url_validator

router = Router()

@router.message(models.broadcastModel.broadcast)
async def broadcastFunction(message: Message, state: FSMContext):
    users = await db.users.get_users_ids()
    sended_count = 0
    for user_id in users:
        try:
            await message.bot.copy_message(user_id, message.chat.id, message.message_id)
            sended_count += 1
        except:
            pass
    await message.answer(f'{sended_count}/{len(users)} пользователям отправлено')
    await state.clear()


@router.message(F.text == '/broadcast')
async def broadcastCommand(message: Message, state: FSMContext):
    if message.chat.id in config.adm_ids:
        await message.answer(replic_broadcastMenu)
        await state.set_state(models.broadcastModel.broadcast)