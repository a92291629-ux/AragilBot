import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = "8243656189:AAHALtgbtUCFYBjc1n3THIsxnFGrqFvDO4k"

print("=" * 50)
print("ЗАПУСК БОТА НА ВЕРСИИ 13.x")
print("=" * 50)

def start_command(update: Update, context: CallbackContext):
    update.message.reply_text('✅ Бот запущен и работает на версии 13.x!')

def echo(update: Update, context: CallbackContext):
    user_message = update.message.text
    update.message.reply_text(f'Вы сказали: {user_message}')

def main():
    try:
        # СТАРЫЙ СИНТАКСИС v13.x
        updater = Updater(TOKEN)
        dispatcher = updater.dispatcher
        
        dispatcher.add_handler(CommandHandler("start", start_command))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
        
        print("Бот успешно запущен...")
        updater.start_polling()
        updater.idle()
        
    except Exception as e:
        print(f"ОШИБКА: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
