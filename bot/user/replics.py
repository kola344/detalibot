from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import db
import config
from aiogram.fsm.context import FSMContext

replic_startCommand = 'Добро пожаловать на курс'
replic_wrong = 'Неправильный ответ. Попробуйте ещё раз'
replic_correct = 'Правильный ответ!'
replic_paymentHave = 'Курс деталиБот. Ниже показаны все видеоуроки'

async def replic_freeVideo_show_markup(video_id: int):
    video = await db.free_videos.getVideo(video_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Открыть', url=video.video_url)]
    ])


# [{question, answers: ['1', '2', '3'], correct_answer: id_answers}]}]
async def replic_show(state: FSMContext):
    state_data = (await state.get_data())['state_data']
    if state_data:
        data = state_data[0]
        if data['type'] == 'video':
            video = await db.free_videos.getVideo(data['data'].video_id)
            state_data.pop(0)
            await state.update_data(state_data=state_data)
            return 'video', video.message_chat_id, video.message_message_id, InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Открыть', url=video.video_url)],
                [InlineKeyboardButton(text='⏩️ Далее', callback_data=f'next.{data["data"].video_id}')]
            ])
        else:
            keyboard = []
            print(data)
            for i, button in enumerate(data['data']['answers']):
                if i == data['data']['correct_answer']:
                    keyboard.append([InlineKeyboardButton(text=button, callback_data=f'correct')])
                else:
                    keyboard.append([InlineKeyboardButton(text=button, callback_data=f'wrong')])
            state_data.pop(0)
            await state.update_data(state_data=state_data)
            return 'test', None, data['data']['question'], InlineKeyboardMarkup(inline_keyboard=keyboard)
    else:
        return 'end', None, f'😄 Отличчно! Вы просмотрели все беслпатные видеоуроки!\nЧтобы получить полный доступ к курсу, вам необходимо оплатить {config.price} рублей.', InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Я оплатил', callback_data='paid')]
        ])



