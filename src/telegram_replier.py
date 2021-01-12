# -*- coding: utf-8 -*-
from bottle import run

import punch_a_clock
import telebot
import mando
import json
import eta


API_TOKEN = json.loads(open('settings.json', 'r').read())['API_TOKEN']

bot = telebot.TeleBot(API_TOKEN)

function = {
    'this is the way': mando.ThisIsTheWay,
    '11620317': punch_a_clock.NexusRPA,
    'eta': eta.CalcETA
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
        bot.send_message(
            message.chat.id, function.get(message.text.lower())().__call__()
        )
    except AttributeError:
        pass
    except TypeError:
        pass
    except Exception as e:
        e.args
        pass


run(bot.polling(none_stop=True), host='localhost', port=8000)
