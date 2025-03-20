import traceback

import db
import config
from bot.admin.tests.replics import *
from bot.admin.tests import keyboards
from bot.admin import models

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.exceptions import TelegramBadRequest

from aiogram.fsm.context import FSMContext

from functions import url_validator

router = Router()

@router.message(models.setTestModel.setTest, F.text)
async def setTestFunc(message: Message, state: FSMContext):
    try:
        questions = []
        splited_questions = message.text.split('\n')
        for question in splited_questions:
            splited = question.split('$')
            print(splited)
            q = splited[0]
            answers = [splited[1], splited[2], splited[3]]
            correct_answer = int(splited[4]) - 1
            validate_correct = answers[correct_answer]
            questions.append({"question": q, "answers": answers, "correct_answer": correct_answer})
        state_data = await state.get_data()
        print(questions)
        await db.tests.add_test(state_data['video_id'], questions)
        await message.answer(await replic_testMenu())
        await state.clear()
    except:
        traceback.print_exc()
        await message.answer(replic_setTestErr)

@router.message(F.text == '/tests')
async def testsCommand(message: Message):
    await message.answer(await replic_testMenu())

@router.message(F.text.startswith('/setTest_'))
async def setTestCommand(message: Message, state: FSMContext):
    video_id = int(message.text.split('_')[1])
    await db.tests.del_all_tests_by_video_id(video_id)
    await message.answer(replic_setTest)
    await state.set_state(models.setTestModel.setTest)
    await state.update_data(video_id=video_id)