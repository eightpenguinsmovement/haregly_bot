#!/usr/bin/env python3
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from telegram import ChatPermissions, ChatMember
import logging
import json
import settings
from random import randint

logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)
updater = None


def haregly(update, context):
    with open("./data/haregly.json", "r") as f:
        json_ = json.loads(f.read())
    sentence = json_[randint(1, len(json_)) - 1]
    context.bot.send_message(update.message.chat.id, sentence)
    context.bot.delete_message(update.message.chat.id, update.message.message_id)


def haregly_latest(update, context):
    with open("./data/haregly.json", "r") as f:
        last_sentence = json.loads(f.read())[-1]
        update.message.reply_text(last_sentence)


def haregly_how_much(update, context):
    with open("./data/haregly.json", "r") as f:
        update.message.reply_text(f"much haregly wow: {len(json.loads(f.read()))}")


def haregly_add(update, context):
    if update.message.from_user.username in settings.ctx.admins:
        with open("./data/haregly.json", "r") as f:
            json_ = json.loads(f.read())
        m = update.message["reply_to_message"]["text"]
        try:
            json_.index(m)
            update.message.reply_text("nie dodawaj takiego gowna")
            return
        except ValueError:
            pass
        json_.append(m)
        json_ = json.dumps(json_, indent=2)
        with open("./data/haregly.json", "w") as f:
            f.write(json_)
        context.bot.delete_message(update.message.chat.id, update.message.message_id)
    else:
        update.message.reply_text("Tylko samedmaxi może dodawać moje wiadomości")


def start(update, context):
    update.message.reply_text(
        f"""dostempne komędy:

haregly
haregly_add
haregly_latest
haregly_how_much
"""
    )


def main():
    global updater
    updater = Updater(settings.TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler(["start", "help"], start))
    dispatcher.add_handler(CommandHandler("haregly", haregly))
    dispatcher.add_handler(CommandHandler("haregly_add", haregly_add))
    dispatcher.add_handler(CommandHandler("haregly_latest", haregly_latest))
    dispatcher.add_handler(CommandHandler("haregly_how_much", haregly_how_much))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
