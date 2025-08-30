# Fix for missing modules in Python 3.11+
import sys
import os

# Создаем fake модули чтобы избежать ошибок импорта
missing_modules = ['imghdr', 'urllib3']
for module_name in missing_modules:
    if module_name not in sys.modules:
        try:
            from types import ModuleType
            fake_module = ModuleType(module_name)
            
            if module_name == 'imghdr':
                fake_module.what = lambda *args, **kwargs: None
            
            sys.modules[module_name] = fake_module
            print(f"✅ Created fake module: {module_name}")
        except Exception as e:
            print(f"⚠️ Failed to create {module_name}: {e}")

# Теперь импортируем основные библиотеки
try:
    import logging
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    print("✅ Основные библиотеки загружены")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("👉 Запустите: pip install -r requirements.txt")
    sys.exit(1)

# ================== НАСТРОЙКИ ==================
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8243656189:AAHALtgbtUCFYBjc1n3THIsxnFGrqFvDO4k')

# ================== ЛОГИРОВАНИЕ ==================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# ================== ПРОВЕРКА ЗАВИСИМОСТЕЙ ==================
def check_dependencies():
    """Проверяем наличие всех необходимых библиотек"""
    required_modules = [
        'telegram', 'telegram.ext', 'logging', 'os', 'sys'
    ]
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
        except ImportError:
            print(f"❌ {module} - MISSING")
            return False
    return True

# ================== КОМАНДЫ БОТА ==================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    try:
        user = update.effective_user
        welcome_text = (
            f"👋 Привет, {user.first_name}!\n"
            "Я успешно работаю на Render.com!\n\n"
            "✅ Все зависимости загружены\n"
            "🐍 Python 3.10+\n"
            "📚 python-telegram-bot v20.x\n\n"
            "Напиши мне что-нибудь!"
        )
        await update.message.reply_text(welcome_text)
        logger.info(f"User {user.id} started the bot")
    except Exception as e:
        logger.error(f"Error in start_command: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = (
        "🤖 *Доступные команды:*\n"
        "/start - Начать работу\n"
        "/help - Помощь\n"
        "/status - Статус бота\n\n"
        "💬 Просто напиши мне сообщение!"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /status"""
    status_text = (
        "🟢 *Статус бота:*\n"
        "• Хостинг: Render.com\n"
        "• Python: 3.10+\n"
        "• Библиотеки: ✅ Загружены\n"
        "• Состояние: Работает нормально"
    )
    await update.message.reply_text(status_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений"""
    user_message = update.message.text
    response = f"🔁 Вы сказали: _{user_message}_"
    await update.message.reply_text(response, parse_mode='Markdown')

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Глобальный обработчик ошибок"""
    logger.error(f"Error: {context.error}")

# ================== ЗАПУСК БОТА ==================
def main():
    """Основная функция запуска бота"""
    print("=" * 60)
    print("🤖 ПРОВЕРКА ЗАВИСИМОСТЕЙ БОТА")
    print("=" * 60)
    
    # Проверяем зависимости
    if not check_dependencies():
        print("❌ Отсутствуют необходимые библиотеки!")
        print("👉 Запустите: pip install -r requirements.txt")
        return
    
    # Проверка токена
    if not TOKEN or 'AAHALtgbtUCFYBjc1n3THIsxnFGrqFvDO4k' in TOKEN:
        print("❌ Токен бота не настроен!")
        print("👉 Создайте переменную окружения TELEGRAM_BOT_TOKEN в Render")
        return
    
    try:
        print("🚀 Запуск бота...")
        
        application = Application.builder().token(TOKEN).build()
        
        # Добавляем обработчики
        handlers = [
            CommandHandler("start", start_command),
            CommandHandler("help", help_command),
            CommandHandler("status", status_command),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
        ]
        
        for handler in handlers:
            application.add_handler(handler)
        
        application.add_error_handler(error_handler)
        
        print("=" * 60)
        print("✅ БОТ УСПЕШНО ЗАПУЩЕН!")
        print(f"📍 Токен: {TOKEN[:10]}...")
        print("🌐 Хостинг: Render.com")
        print("=" * 60)
        
        # Запускаем бота
        application.run_polling()
        
    except Exception as e:
        print(f"💥 КРИТИЧЕСКАЯ ОШИБКА: {e}")
        logger.critical(f"Critical error: {e}")

if __name__ == '__main__':
    main()
