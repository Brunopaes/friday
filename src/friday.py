# -*- coding: utf-8 -*-
import skill_caller
import helpers
import telebot


friday = telebot.TeleBot(
    **helpers.read_json('settings/telegram_settings.json')
)


functions = {
    'this is the way': skill_caller.return_mando,
    'ponto': skill_caller.return_punch_a_clock,
    'eta': skill_caller.return_eta,
    'ps5': skill_caller.return_tweet,
    'add me': skill_caller.return_user_alert,
    'drop me': skill_caller.return_user_alert,
    'va se foder': skill_caller.return_galo_tarsilo,
}

arg_functions = {
    'morse': skill_caller.return_morse,
    'coke': skill_caller.return_coke,
    'btc': skill_caller.return_btc,
    'porn': skill_caller.return_cantina_band,
}

media_functions = {
    'r/': skill_caller.return_reddit,
}


@friday.message_handler(func=lambda message: True)
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
            friday.send_message(
                message.chat.id,
                arg_functions.get(msg[0])(message)
            )
        else:
            friday.send_message(
                message.chat.id,
                functions.get(msg[0])(message)
            )
    except TypeError:
        try:
            friday.send_message(
                message.chat.id,
                functions.get(' '.join(msg))(message)
            )
        except TypeError:
            try:
                friday.send_photo(
                    message.chat.id,
                    media_functions.get(
                        'r/' if msg[0].startswith('r/') else msg[0]
                    )(message),
                    caption='Random submission form {}'.format(msg[0])
                    if msg[0].startswith('/r') else ''
                )
            except telebot.apihelper.ApiException:
                friday.send_message(
                    message.chat.id,
                    'Impossible, perhaps the archives are incomplete!'
                )
            except TypeError as e:
                e.args
    except AttributeError as e:
        e.args
    except Exception as e:
        e.args

    helpers.StoreMetadata(message.json).__call__()


while True:
    try:
        friday.polling()
    except Exception as error:
        error.args
