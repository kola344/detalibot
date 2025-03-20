import db
import config
from bot.admin.replics import *
from bot.admin import keyboards, models

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram import F

from aiogram.fsm.context import FSMContext

router = Router()

@router.message(F.text == '/admin')
async def adminCommand(message: Message, state: FSMContext):
    await state.clear()
    if message.chat.id in config.adm_ids:
        await message.answer(replic_adminHelp)

@router.callback_query(F.data == 'closeMenu')
async def closeMenu(call: CallbackQuery):
    await call.message.delete()
    await call.answer(replic_closed)
