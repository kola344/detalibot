from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import db
import config

replic_closed = '🙂‍↕️ Closed'

replic_adminHelp = '''
Команды администратора:
/free_videos - открыть редактор бесплатных видео
/videos - открыть редактор платных видео
/tests - открыть редактор тестов, отправляющихся после просмотра бесплатных видео
/usersCount - получить количество пользователей
/users - получить список пользователей
/broadcast - разослать сообщение всем пользователям
/paymentsCount - получить количество платежей
/payments - получить список платежей
'''