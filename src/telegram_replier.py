# -*- coding: utf-8 -*-
import telebot
import json


API_TOKEN = json.loads(open('settings.json', 'r').read())['API_TOKEN']

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    """This function gets the incoming message and replies with it.

    Parameters
    ----------
    message : telebot.types.Message
        The message object.

    """
    bot.send_message(message.chat.id, message.text)


bot.polling()
