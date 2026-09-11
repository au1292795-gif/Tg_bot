import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler

TOKEN = '8617582353:AAGRmkZ9c6X_qwKgIcjmI-c7wL9wKLQz1rQ'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

PHONE, NAME = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton("Отправить номер телефона", request_contact=True)
    keyboard = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        "Здравствуйте! Для продолжения работы авторизуйтесь и отправьте ваш номер.",
        reply_markup=keyboard
    )
    return PHONE

async def receive_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    context.user_data['phone'] = contact.phone_number
    
    await update.message.reply_text(
        "Спасибо! Теперь введите ваше имя:",
        reply_markup=ReplyKeyboardRemove()
    )
    return NAME

async def receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    phone = context.user_data.get('phone')
    
    await update.message.reply_text("Ваша заявка принята! Спасибо.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Действие отменено.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PHONE: [MessageHandler(filters.CONTACT, receive_contact)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(conv_handler)
    app.run_polling()
