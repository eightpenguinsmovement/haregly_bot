from telegram import Update
from telegram.ext import CallbackContext
from tinydb import Query
from random import randint
from . import bot, db
from .functions import send_haregly
from .config import ADMINS_IDS


@bot.command("haregly", help="moja losowa wiadomość")
def haregly(update: Update, context: CallbackContext):
    random_id = randint(0, len(db))
    sentence = db.all()[random_id]["msg"]
    send_haregly(update, context, sentence)


@bot.command(
    "haregly_latest", help="ostatnia wiadomość kturom samedmaxi dodał do spajłeru"
)
def haregly_latest(update: Update, context: CallbackContext):
    sentence = db.all()[-1]["msg"]
    send_haregly(update, context, sentence)


@bot.command("haregly_how_much", help="jak dużo moich wiadomości jest dodanych")
def haregly_how_much(update: Update, context: CallbackContext):
    update.message.reply_text(f"much haregly wow: {len(db)}")


@bot.command("haregly_add", help="dodawanie wiadomości do spajłeru")
def haregly_add(update: Update, context: CallbackContext):
    if update.message.from_user.id not in ADMINS_IDS:
        update.message.reply_text("tylko samedmaxi może dodawać moje wiadomości")
        return

    try:
        message = update.message["reply_to_message"]["text"]
    except TypeError:
        return

    q = Query()
    if len(db.search(q.msg == message)) == 0:
        db.insert({"msg": message})
        context.bot.delete_message(
            update.message.chat.id, update.message.message_id
        )
    else:
        update.message.reply_text("nie dodawaj takiego gówna")


@bot.custom_help_command
def help(update: Update, context: CallbackContext, commands):
    help_message = "Dostempne komędy:\n\n"
    for cmd, desc in commands.items():
        help_message += f"/{cmd}\n{desc}\n\n"
    update.message.reply_text(help_message)
