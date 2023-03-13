import json
import random
import os
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
)


# create Bot
with open("token.json", "r") as read_file:
    TOKEN = json.load(read_file)[0]
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


# define answer weights
with open("answer_weights.json", "r") as read_file:
    weights = json.load(read_file)

# fill answers list
answers = []
for answer, weight in weights.items():
    for i in range(0, weight):
        answers.append(answer)

# load sweet text
with open("sweet_texts.json", "r") as read_file:
    sweet_texts = json.load(read_file)

# load emoijs
with open("emoijs.json", "r") as read_file:
    emoijs = json.load(read_file)


# load pics

pics = []
for file in os.listdir("pics"):
    pics.append(file)


def generate_muh():
    muh = "M"
    for i in range(0, random.randrange(1, 5)):
        muh += "u"

    for i in range(0, random.randrange(1, 5)):
        muh += "h"

    return muh


def generate_uh():
    uh = "Ü"
    for i in range(0, random.randrange(0, 4)):
        uh += "ü"

    for i in range(0, random.randrange(1, 5)):
        uh += "h"

    return uh + "!"


def sweet_text_no_empty():
    text = random.choice(sweet_texts)

    for i in range(0, random.randrange(0, 4)):
        text += random.choice(emoijs)

    return text


def sweet_text():
    text = ""
    if random.randrange(0, 1) == 1:
        text += random.choice(sweet_texts)

    for i in range(0, random.randrange(0, 4)):
        text += random.choice(emoijs)

    return text


def get_pic():
    return "pics/" + random.choice(pics)


def answer_handler(bot, update):
    answer = random.choice(answers)
    if answer == "muh":
        bot.send_message(update.message.from_user.id, text=generate_muh())

    if answer == "üh":
        bot.send_message(update.message.from_user.id, text=generate_uh())

    if answer == "sweet":
        bot.send_message(update.message.from_user.id, text=sweet_text_no_empty())

    if answer == "pic":
        bot.send_photo(
            update.message.from_user.id,
            photo=open(get_pic(), "rb"),
            caption=sweet_text(),
        )


# register handler for plain messages
dispatcher.add_handler(MessageHandler(Filters.text, answer_handler))

telegramBot = updater.bot
updater.start_polling()
