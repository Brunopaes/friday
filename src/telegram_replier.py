# -*- coding: utf-8 -*-
import skill_caller
import helpers
import telebot


bot = telebot.TeleBot(**helpers.read_json('settings.json'))

functions = {
    'this is the way': skill_caller.return_mando,
    'ponto': skill_caller.return_punch_a_clock,
    'eta': skill_caller.return_eta,
    'ps5': skill_caller.return_tweet,
    'add me': skill_caller.return_user_alert,
    'drop me': skill_caller.return_user_alert,
}

arg_functions = {
    'morse': skill_caller.return_morse,
    'coke': skill_caller.return_coke,
    'btc': skill_caller.return_btc
}


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    """This function gets the incoming message and calls the respective skill.

    Parameters
    ----------
    message : telebot.types.Message
        The message object.

    """
    msg = message.text.lower().split(' ')
    try:
        if len(message.text.split(' ')) > 1:
            bot.send_message(
                message.chat.id,
                arg_functions.get(msg[0])(message)
            )
        else:
            bot.send_message(
                message.chat.id,
                functions.get(msg[0])(message)
            )
    except TypeError:
        try:
            bot.send_message(
                message.chat.id,
                functions.get(' '.join(msg))(message)
            )
        except TypeError as e:
            e.args
    except AttributeError as e:
        e.args
    except Exception as e:
        e.args


bot.polling()
