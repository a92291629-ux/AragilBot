import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ПРЯМОЕ УКАЗАНИЕ ТОКЕНА ДЛЯ ПРОВЕРКИ
TOKEN = "8243656189:AAHALtgbtUCFYBjc1n3THIsxnFGrqFvDO4k"

print("=" * 50)
print("ЗАПУСК БОТА")
print(f"Токен: {TOKEN}")
print("=" * 50)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('✅ Бот запущен и работает!')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text(f'Вы сказали: {user_message}')

def main():
    try:
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler('start', start_command))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        
        print("Бот успешно запущен...")
        app.run_polling()
        
    except Exception as e:
        print(f"ОШИБКА: {e}")
        print("Проверьте токен и настройки")

if __name__ == '__main__':
    main()
