from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import db
import config

replic_setTest = '''
Заполните тест в следующем формате:
Вопрос 1 $ Вариант ответа 1 $ Вариант ответа 2 $ Вариант ответа 3 $ 2
Вопрос 2 $ Вариант ответа 1 $ Вариант ответа 2 $ Вариант ответа 3 $ 1
Вопрос 3 $ Вариант ответа 1 $ Вариант ответа 2 $ Вариант ответа 3 $ 3
Где разделитель - $, в начале идет вопрос, затем 3 варианта ответа, а в конце - номер правильного ответа.
Каждый новый вопрос с новой строки.
'''

replic_setTestErr = 'Неверный формат, попробуйте еше раз'

async def replic_testMenu():
    free_videos = await db.free_videos.getVideos()
    text = 'Чтобы установить тест для определенного бесплатного видео, введите команду\n/setTest_<id видео>\n'
    add_text = '\n'.join([f"/setTest_{video.video_id} - {'Тест установлен' if await db.tests.check_test_by_video_id(video.video_id) else 'Тест не установлен'}" for video in free_videos])
    return text + add_text
