import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получаем токен из переменных окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Проверяем, что токен существует
if not TOKEN:
    logger.error("Токен не найден! Убедитесь, что переменная окружения TELEGRAM_BOT_TOKEN установлена.")
    exit(1)

# Команда /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        f"Привет, {user.mention_html()}! 👋\n"
        "Я простой эхо-бот, работающий на Render.com!\n\n"
        "Просто напиши мне что-нибудь, и я повторю это."
    )
    logger.info(f"User {user.id} started the bot")

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🤖 Доступные команды:
/start - Начать работу с ботом
/help - Показать эту справку
/about - Информация о боте

Просто отправь мне любое сообщение, и я отвечу!
    """
    await update.message.reply_text(help_text)
    logger.info("Help command executed")

# Команда /about
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = """
ℹ️ Обо мне:
• Создан на Python с использованием python-telegram-bot
• Хостится на Render.com
• Исходный код: https://github.com/ваш-username/ваш-репозиторий
    """
    await update.message.reply_text(about_text)

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user = update.effective_user
    
    # Простой эхо-ответ
    response = f"🔁 Вы сказали: {user_message}"
    
    await update.message.reply_text(response)
    logger.info(f"User {user.id} sent message: {user_message}")

# Обработка ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Ошибка при обработке update {update}: {context.error}")

# Основная функция
def main():
    try:
        logger.info("Запуск бота...")
        
        # Создаем приложение
        application = Application.builder().token(TOKEN).build()
        
        # Добавляем обработчики команд
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("about", about_command))
        
        # Добавляем обработчик текстовых сообщений
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Добавляем обработчик ошибок
        application.add_error_handler(error_handler)
        
        # Запускаем бота
        logger.info("Бот запущен и готов к работе!")
        print("=" * 50)
        print("🤖 Бот успешно запущен!")
        print("📍 Хостинг: Render.com")
        print("🐍 Версия Python: 3.10+")
        print("📚 Библиотека: python-telegram-bot v20.x")
        print("=" * 50)
        
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Критическая ошибка при запуске: {e}")
        print(f"❌ Ошибка: {e}")

if __name__ == '__main__':
    main()
