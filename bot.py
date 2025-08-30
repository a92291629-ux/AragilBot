import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Токен, который вы получили от BotFather
TOKEN = os.getenv('8243656189:AAHALtgbtUCFYBjc1n3THIsxnFGrqFvDO4k')  # Теперь os.getenv будет работать!

# === ДОБАВЬТЕ ЭТУ ПРОВЕРКУ ===
if TOKEN is None:
    raise ValueError("Токен не найден! Проверьте переменную окружения TOKEN.")
# =============================

# Обработчик команды /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я бот. Спасибо, что запустили меня!')

# Обработчик обычных текстовых сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text(f'Вы сказали: {user_message}')

# Основная функция
def main():
    # Создаем Application и передаем ему токен
    app = Application.builder().token(TOKEN).build()

    # Добавляем обработчики команд и сообщений
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запускаем бота в режиме постоянного опроса (Polling)
    print('Бот запущен...')
    app.run_polling()

if __name__ == '__main__':
    main()
