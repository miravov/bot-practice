import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import nltk
from nltk.chat.util import Chat, reflections
import os
from dotenv import load_dotenv

load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Загрузка необходимых данных NLTK
nltk.download('punkt')

# Определение шаблонов и ответов для чат-бота
patterns = [
    (r'привет|здравствуй|хай|хелло',
     ['Привет!', 'Здравствуйте!', 'Приветствую!']),
    
    (r'как дела|как ты|как поживаешь',
     ['Отлично! А у вас как дела?', 'Все хорошо! Как ваши дела?', 'Замечательно! А у вас как?']),
    
    (r'хорошо|отлично|замечательно',
     ['Это здорово!', 'Рад это слышать!', 'Очень приятно!']),
    
    (r'плохо|ужасно|не очень',
     ['Не переживайте, все наладится!', 'Главное - не сдаваться!', 'Держитесь!']),
    
    (r'пока|до свидания|до встречи',
     ['До свидания!', 'Всего доброго!', 'До встречи!']),
    
    (r'.*',
     ['Интересно...', 'Расскажите подробнее', 'Понятно...'])
]

# Создание объекта чат-бота
chatbot = Chat(patterns, reflections)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start - отправляет приветственное сообщение"""
    await update.message.reply_text(
        'Привет! Я простой чат-бот. Давай пообщаемся!'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help - отправляет справку по использованию бота"""
    await update.message.reply_text(
        'Просто напиши мне сообщение, и я постараюсь ответить!'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик входящих сообщений - генерирует ответ на основе шаблонов"""
    user_message = update.message.text.lower()
    response = chatbot.respond(user_message)
    await update.message.reply_text(response)

def main():
    """Основная функция для запуска бота"""
    # Создание приложения и передача токена бота
    application = (
        Application.builder()
        .token(os.getenv('TELEGRAM_BOT_TOKEN'))
        .build()
    )
    
    # Добавление обработчиков команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 