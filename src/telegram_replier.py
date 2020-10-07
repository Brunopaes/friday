# -*- coding: utf-8 -*-
import punch_a_clock
import telebot
import json


API_TOKEN = json.loads(open('settings.json', 'r').read())['API_TOKEN']

bot = telebot.TeleBot(API_TOKEN)

function = {
    'ponto': punch_a_clock.NexusRPA
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
        bot.send_message(message.chat.id, 'Function does not exists!')
    except TypeError:
        bot.send_message(message.chat.id, 'Function does not exists!')


bot.polling(none_stop=True)
