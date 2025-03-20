import asyncio

import db
import config
from bot.user.replics import *
from bot.user import keyboards, models

from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F

from aiogram.fsm.context import FSMContext

router = Router()
#state
# data = [{"type": "video", "data": video}, {"type": "question": "data": question

@router.message(F.text == '/start')
async def startCommand(message: Message, state: FSMContext):
    await db.users.add_user(message.chat.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    if await db.payments.check_payment(message.chat.id):
        await message.answer(replic_paymentHave)
        free_videos = await db.free_videos.getVideos()
        videos = await db.videos.getVideos()
        for free_video in free_videos:
            await message.bot.copy_message(message.chat.id, free_video.message_chat_id, free_video.message_message_id,
                                                 reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                     [InlineKeyboardButton(text='Открыть', url=free_video.video_url)]
                                                 ]))
        for video in videos:
            await message.bot.copy_message(message.chat.id, video.message_chat_id, video.message_message_id,
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                            [InlineKeyboardButton(text='Открыть', url=video.video_url)]
                                        ]))
        return
    await message.answer(replic_startCommand)
    await state.set_state(models.userModel.course)
    free_videos = await db.free_videos.getVideos()
    state_data = []
    for free_video in free_videos:
        state_data.append({"type": "video", "data": free_video})
        if await db.tests.check_test_by_video_id(free_video.video_id):
            test = await db.tests.get_test_data_by_video_id(free_video.video_id)
            if test:
                for question in test:
                    if question:
                        state_data.append({"type": "question", "data": question})
    await state.update_data(state_data=state_data)
    await state.set_state(models.userModel.course)
    data_type, chat, mess, markup = await replic_show(state)
    await message.bot.copy_message(message.chat.id, chat, mess, reply_markup=markup)

@router.callback_query(F.data.startswith('next'))
async def nextCallback(call: CallbackQuery, state: FSMContext):
    video_id = int(call.data.split(".")[1])
    await call.message.edit_reply_markup(reply_markup=await replic_freeVideo_show_markup(video_id))
    data_type, chat, mess, markup = await replic_show(state)
    if data_type == "video":
        await call.message.bot.copy_message(call.message.chat.id, chat, mess, reply_markup=markup)
    elif data_type == "test":
        await call.message.answer(mess, reply_markup=markup)
    else:
        await call.message.answer(mess, reply_markup=markup)

@router.callback_query(F.data == 'correct')
async def nextCallback(call: CallbackQuery, state: FSMContext):
    data_type, chat, mess, markup = await replic_show(state)
    await call.message.edit_text('Это правильный ответ!')
    if data_type == "video":
        await call.message.bot.copy_message(call.message.chat.id, chat, mess, reply_markup=markup)
    elif data_type == "test":
        await call.message.answer(mess, reply_markup=markup)
    else:
        await call.message.answer(mess, reply_markup=markup)

@router.callback_query(F.data == 'wrong')
async def nextCallback(call: CallbackQuery, state: FSMContext):
    await call.answer('Это неправильный ответ!', show_alert=True)
    await asyncio.sleep(3)
    await call.message.copy_to(call.from_user.id)

@router.callback_query(F.data == 'paid')
async def paidCallback(call: CallbackQuery, state: FSMContext):
    videos = await db.videos.getVideos()
    for video in videos:
        await call.bot.copy_message(call.from_user.id, video.message_chat_id, video.message_message_id, reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Открыть', url=video.video_url)]
    ]))
    await db.payments.add_payment(call.from_user.id, config.price)



