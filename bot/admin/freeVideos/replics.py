from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import db
import config

replic_deleted = '🙂‍↕️ Deleted'
replic_alreadyDeleted = '🙂‍↕️ Already deleted'

replic_addVideo = 'Отправьте сообщение, которое будет пересылаться пользователям'
replic_addUrl = 'Сообщение получено. Отправьте URL Видео'
replic_urlInvalid = 'URL не валид'

async def replic_freeVideos():
    videos = await db.free_videos.getVideos()
    keyboard = []
    for i, video in enumerate(videos):
        keyboard.append([InlineKeyboardButton(text=f'Видео {video.video_id}', callback_data=f'adm.eFreeV.{video.video_id}')])
    keyboard.append([InlineKeyboardButton(text='➕ Добавить видео', callback_data='adm.addEfreeV')])
    keyboard.append([InlineKeyboardButton(text='❌ Удалить все видео', callback_data=f'adm.delFreeV')])
    keyboard.append([InlineKeyboardButton(text='✖️ Закрыть меню', callback_data='closeMenu')])
    return 'Меню бесплатных видео', InlineKeyboardMarkup(inline_keyboard=keyboard)

async def replic_video_show(video_id: int):
    video = await db.free_videos.getVideo(video_id)
    return video.message_chat_id, video.message_message_id, InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Открыть', url=video.video_url)],
        [InlineKeyboardButton(text='⬅️ Назад', callback_data='freeVideos')]
    ])