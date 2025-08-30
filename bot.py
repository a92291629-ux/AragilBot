from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Замените 'YOUR_TOKEN' на токен, полученный от @BotFather
TOKEN = os.getenv('8243656189:AAHALtgbtUCFYBjc1n3THIsxnFGrqFvDO4k')
BOT_USERNAME = '@aragilmarket_bot'

# Обработчик команды /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я простой бот. Как дела?')

# Обработчик команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Я могу отвечать на сообщения! Напишите что-нибудь.')

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    if 'привет' in text:
        response = 'И тебе привет!'
    elif 'как дела' in text:
        response = 'Отлично, спасибо! А у тебя?'
    else:
        response = 'Не совсем понимаю, о чем вы...'
    
    await update.message.reply_text(response)

# Обработчик ошибок
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Запуск бота...')
    app = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики команд
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    
    # Добавляем обработчик сообщений
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Добавляем обработчик ошибок
    app.add_error_handler(error)
    
    # Опрашиваем сервер Telegram на наличие новых сообщений
    print('Ожидание сообщений...')
    app.run_polling(poll_interval=3)