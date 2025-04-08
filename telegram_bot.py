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
    (r'привет|здравствуй|хай|хелло|доброе утро|добрый день|добрый вечер',
     ['Привет! Рад вас видеть!', 'Здравствуйте! Как я могу вам помочь?', 'Приветствую! Чем могу быть полезен?']),
    
    (r'как дела|как ты|как поживаешь|как твои дела',
     ['Отлично! А у вас как дела?', 'Все хорошо! Как ваши дела?', 'Замечательно! Расскажите, как у вас дела?']),
    
    (r'хорошо|отлично|замечательно|прекрасно|супер',
     ['Это здорово! Рад за вас!', 'Рад это слышать! Продолжайте в том же духе!', 'Очень приятно! Желаю вам дальнейших успехов!']),
    
    (r'плохо|ужасно|не очень|так себе|неважно',
     ['Не переживайте, все наладится!', 'Главное - не сдаваться! Я верю в вас!', 'Держитесь! Всё пройдет, и солнце снова засияет!']),
    
    (r'пока|до свидания|до встречи|прощай|всего доброго',
     ['До свидания! Буду рад пообщаться снова!', 'Всего доброго! Возвращайтесь скорее!', 'До встречи! Хорошего дня!']),
    
    (r'спасибо|благодарю|ты мне помог',
     ['Пожалуйста! Рад был помочь!', 'Обращайтесь! Всегда готов помочь!', 'Не за что! Буду рад помочь снова!']),
    
    (r'кто ты|расскажи о себе|что ты умеешь',
     ['Я ваш виртуальный помощник! Я могу поддержать беседу и помочь вам в различных вопросах.', 
      'Я чат-бот, созданный для общения и помощи. Давайте познакомимся!',
      'Я ваш дружелюбный собеседник. Могу поддержать разговор и помочь вам!']),
    
    (r'шутки|анекдот|расскажи шутку',
     ['Знаете, почему программисты не любят природу? Там слишком много багов! 😄',
      'Как называется кот, который сидит на сервере? Кот-админ! 😺', ]),
    
    (r'.*',
     ['Интересно... Расскажите подробнее!', 'Понятно... А что вы об этом думаете?', 'Хм, любопытно! Давайте обсудим это подробнее.'])
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