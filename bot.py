# Fix for Python 3.11+ compatibility
import sys
if 'imghdr' not in sys.modules:
    # Create a fake imghdr module to avoid errors
    from types import ModuleType
    imghdr_module = ModuleType('imghdr')
    
    def what(*args, **kwargs):
        """Mock function for deprecated imghdr.what"""
        return None
    
    imghdr_module.what = what
    sys.modules['imghdr'] = imghdr_module

import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ================== НАСТРОЙКИ ==================
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8243656189:AAHALtgbtUCFYBjc1n3THIsxnFGrqFvDO4k')

# ================== ЛОГИРОВАНИЕ ==================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ================== КОМАНДЫ БОТА ==================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    try:
        user = update.effective_user
        welcome_text = (
            f"👋 Привет, {user.first_name}!\n"
            "Я работающий бот на Python!\n\n"
            "📝 Просто напиши мне сообщение, и я отвечу!\n"
            "🆘 Напиши /help для списка команд"
        )
        await update.message.reply_text(welcome_text)
        logger.info(f"User {user.id} started the bot")
    except Exception as e:
        logger.error(f"Error in start_command: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    try:
        help_text = (
            "🤖 *Доступные команды:*\n"
            "/start - Начать работу\n"
            "/help - Помощь\n"
            "/info - Информация\n\n"
            "💬 Просто напиши мне что-нибудь!"
        )
        await update.message.reply_text(help_text, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error in help_command: {e}")

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /info"""
    try:
        info_text = (
            "ℹ️ *Информация о боте:*\n"
            "• Python + python-telegram-bot\n"
            "• Хостинг: Render.com\n"
            "• Версия: 1.0\n"
            "• Статус: ✅ Работает"
        )
        await update.message.reply_text(info_text, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error in info_command: {e}")

# ================== ОБРАБОТКА СООБЩЕНИЙ ==================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений"""
    try:
        user_message = update.message.text
        user = update.effective_user
        
        if user_message:
            response = f"🔁 Ты написал: _{user_message}_"
            await update.message.reply_text(response, parse_mode='Markdown')
            logger.info(f"User {user.id}: {user_message}")
        else:
            await update.message.reply_text("Отправь текстовое сообщение! 📝")
            
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        await update.message.reply_text("❌ Произошла ошибка при обработке сообщения")

# ================== ОБРАБОТКА ОШИБОК ==================
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Глобальный обработчик ошибок"""
    try:
        logger.error(f"Update {update} caused error {context.error}")
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "⚠️ Произошла техническая ошибка. Попробуйте позже."
            )
    except Exception as e:
        logger.error(f"Error in error_handler: {e}")

# ================== ЗАПУСК БОТА ==================
def main():
    """Основная функция запуска бота"""
    try:
        # Проверка токена
        if not TOKEN or TOKEN == '8243656189:AAHALtgbtUCFYBjc1n3THIsxnFGrqFvDO4k':
            logger.error("❌ Токен бота не настроен!")
            print("=" * 60)
            print("🚨 ОШИБКА: Токен бота не найден!")
            print("👉 Создайте переменную окружения TELEGRAM_BOT_TOKEN")
            print("👉 В настройках Render добавьте ваш токен от @BotFather")
            print("=" * 60)
            return
        
        logger.info("🚀 Запуск бота...")
        
        # Создаем приложение
        application = Application.builder().token(TOKEN).build()
        
        # Добавляем обработчики
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("info", info_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_error_handler(error_handler)
        
        # Информация о запуске
        print("=" * 60)
        print("🤖 БОТ УСПЕШНО ЗАПУЩЕН!")
        print(f"📍 Токен: {TOKEN[:10]}...")
        print("🐍 Python: 3.10+")
        print("📚 Библиотека: python-telegram-bot v20.x")
        print("🌐 Хостинг: Render.com")
        print("=" * 60)
        
        logger.info("✅ Бот запущен и готов к работе!")
        
        # Запускаем опрос
        application.run_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES
        )
        
    except Exception as e:
        logger.critical(f"❌ Критическая ошибка при запуске: {e}")
        print(f"💥 КРИТИЧЕСКАЯ ОШИБКА: {e}")
        print("👉 Проверьте токен и настройки")

if __name__ == '__main__':
    main()
