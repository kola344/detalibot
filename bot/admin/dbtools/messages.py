import db
import config
from bot.admin.dbtools.replics import *
from bot.admin.dbtools import keyboards
from bot.admin import models

from aiogram import Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import F
from aiogram.exceptions import TelegramBadRequest

from aiogram.fsm.context import FSMContext

from functions import url_validator

router = Router()

@router.message(F.text == '/usersCount')
async def usersCountCommand(message: Message):
    if message.chat.id in config.adm_ids:
        count = await db.users.get_users_count()
        await message.answer(f'Количество пользователей: {count}')

@router.message(F.text == '/users')
async def usersCommand(message: Message):
    if message.chat.id in config.adm_ids:
        list_path = await db.users.get_users_list()
        await message.answer_document(FSInputFile(list_path))

@router.message(F.text == '/paymentsCount')
async def paymentsCountCommand(message: Message):
    if message.chat.id in config.adm_ids:
        count, summ = await db.payments.get_payments_count()
        await message.answer(f'Количество платежей: {count}\nСумма: {summ}')

@router.message(F.text == '/payments')
async def paymentsCommand(message: Message):
    if message.chat.id in config.adm_ids:
        list_path = await db.payments.get_payments()
        await message.answer_document(FSInputFile(list_path))