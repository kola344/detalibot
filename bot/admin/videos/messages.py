import db
import config
from bot.admin.videos.replics import *
from bot.admin.videos import keyboards
from bot.admin import models

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.exceptions import TelegramBadRequest

from aiogram.fsm.context import FSMContext

from functions import url_validator

router = Router()

@router.message(models.addVideo.addURL, F.text)
async def addVideoURLFunc(message: Message, state: FSMContext):
    state_data = await state.get_data()
    if await url_validator.validate_url(message.text):
        await db.videos.addVideo(message.chat.id, state_data['message_id'], message.text)
        text, markup = await replic_Videos()
        await message.answer(text, reply_markup=markup)
        await state.clear()
        return
    await message.answer(replic_urlInvalid)

@router.message(models.addVideo.addMessage)
async def addVideoMessageFunc(message: Message, state: FSMContext):
    await state.update_data(message_id=message.message_id)
    await message.answer(replic_addUrl)
    await state.set_state(models.addVideo.addURL)

@router.message(F.text == '/videos')
async def VideosCommand(message: Message):
    if message.chat.id in config.adm_ids:
        text, markup = await replic_Videos()
        await message.answer(text, reply_markup=markup)

@router.callback_query(F.data == 'videos')
async def Videos(call: CallbackQuery):
    text, markup = await replic_Videos()
    await call.message.delete()
    await call.message.answer(text, reply_markup=markup)

@router.callback_query(F.data == 'adm.delV')
async def delV(call: CallbackQuery):
    await db.videos.delVideos()
    try:
        text, markup = await replic_Videos()
        await call.message.edit_text(text, reply_markup=markup)
        await call.answer(replic_deleted)
    except TelegramBadRequest:
        await call.answer(replic_alreadyDeleted)

@router.callback_query(F.data == 'adm.addEV')
async def addEV(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(replic_addVideo)
    await state.set_state(models.addVideo.addMessage)

@router.callback_query(F.data.startswith('adm.eV.'))
async def eV(call: CallbackQuery):
    video_id = int(call.data.split('.')[2])
    chat_id, message_id, markup = await replic_video_show(video_id)
    await call.message.delete()
    await call.bot.copy_message(call.from_user.id, chat_id, message_id, reply_markup=markup)