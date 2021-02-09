# -*- coding: utf-8 -*-
from bottle import run

import skill_caller
import telebot
import json


API_TOKEN = json.loads(open('settings.json', 'r').read())['API_TOKEN']

bot = telebot.TeleBot(API_TOKEN)

functions = {
    'this is the way': skill_caller.return_mando,
    '11620317': skill_caller.return_punch_a_clock,
    'eta': skill_caller.return_eta,
    'btc': skill_caller.return_btc
}

arg_functions = {
    'morse': skill_caller.return_morse,
    'coke': skill_caller.return_coke
}


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    """This function gets the incoming message and replies with it.

    Parameters
    ----------
    message : telebot.types.Message
        The message object.

    """
    try:
        if len(message.text.split(' ')) > 1:
            msg = message.text.lower().split(' ')
            bot.send_message(
                message.chat.id,
                arg_functions.get(msg[0])(' '.join(msg[1:]))
            )
        else:
            bot.send_message(
                message.chat.id,
                functions.get(message.text.lower())()
            )
    except TypeError as e:
        e.args


run(bot.polling(none_stop=True), host='localhost', port=8000)
