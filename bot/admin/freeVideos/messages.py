import db
import config
from bot.admin.freeVideos.replics import *
from bot.admin.freeVideos import keyboards
from bot.admin import models

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.exceptions import TelegramBadRequest

from aiogram.fsm.context import FSMContext

from functions import url_validator

router = Router()

@router.message(models.addVideoFreeModel.addURL, F.text)
async def addVideoFreeURLFunc(message: Message, state: FSMContext):
    state_data = await state.get_data()
    if await url_validator.validate_url(message.text):
        await db.free_videos.addVideo(message.chat.id, state_data['message_id'], message.text)
        text, markup = await replic_freeVideos()
        await message.answer(text, reply_markup=markup)
        await state.clear()
        return
    await message.answer(replic_urlInvalid)

@router.message(models.addVideoFreeModel.addMessage)
async def addVideoFreeMessageFunc(message: Message, state: FSMContext):
    await state.update_data(message_id=message.message_id)
    await message.answer(replic_addUrl)
    await state.set_state(models.addVideoFreeModel.addURL)

@router.message(F.text == '/free_videos')
async def freeVideosCommand(message: Message):
    if message.chat.id in config.adm_ids:
        text, markup = await replic_freeVideos()
        await message.answer(text, reply_markup=markup)

@router.callback_query(F.data == 'freeVideos')
async def freeVideos(call: CallbackQuery):
    text, markup = await replic_freeVideos()
    await call.message.delete()
    await call.message.answer(text, reply_markup=markup)

@router.callback_query(F.data == 'adm.delFreeV')
async def delFreeV(call: CallbackQuery):
    await db.free_videos.delVideos()
    try:
        text, markup = await replic_freeVideos()
        await call.message.edit_text(text, reply_markup=markup)
        await call.answer(replic_deleted)
    except TelegramBadRequest:
        await call.answer(replic_alreadyDeleted)

@router.callback_query(F.data == 'adm.addEfreeV')
async def addEfreeV(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(replic_addVideo)
    await state.set_state(models.addVideoFreeModel.addMessage)

@router.callback_query(F.data.startswith('adm.eFreeV.'))
async def eFreeV(call: CallbackQuery):
    video_id = int(call.data.split('.')[2])
    chat_id, message_id, markup = await replic_video_show(video_id)
    await call.message.delete()
    await call.bot.copy_message(call.from_user.id, chat_id, message_id, reply_markup=markup)
