from telegram import Update
from telegram.ext import CallbackContext


def send_haregly(update: Update, context: CallbackContext, sentence: str):
    chat_id = update.message.chat.id
    try:
        reply_id = update.message["reply_to_message"].message_id
    except AttributeError:
        reply_id = None

    context.bot.send_message(chat_id, sentence, reply_to_message_id=reply_id)
    context.bot.delete_message(chat_id, update.message.message_id)
