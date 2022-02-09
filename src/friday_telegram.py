# -*- coding: utf-8 -*-
import helpers
import telebot

import skills


friday = telebot.TeleBot(
    **helpers.read_json('settings/telegram_settings.json')
)

functions = skills.functions
arg_functions = skills.arg_functions
media_functions = skills.media_functions


@friday.message_handler(func=lambda message: True)
def message_handler(message):
    """This function gets the incoming message and calls the respective
    skill.

    Parameters
    ----------
    message : telebot.types.Message
        The message object.

    """
    payload = helpers.TelegramPayloadParser(message).__call__()
    message_text = payload.get('message').lower().split(' ')
    try:
        if len(message.text.split(' ')) > 1:
            friday.send_message(
                message.chat.id,
                arg_functions.get(message_text[0])(payload)
            )
        else:
            friday.send_message(
                message.chat.id,
                functions.get(message_text[0])(payload)
            )
    except TypeError:
        try:
            friday.send_message(
                message.chat.id,
                functions.get(' '.join(message_text))(payload)
            )
        except TypeError:
            try:
                friday.send_photo(
                    message.chat.id,
                    media_functions.get(
                        'r/' if message_text[0].startswith('r/')
                        else message_text[0]
                    )(payload),
                    caption='Random submission form {}'.format(
                        message_text[0]
                    ) if message_text[0].startswith('r/') else ''
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

    helpers.StoreMetadata(payload).__call__()


while True:
    try:
        friday.polling()
    except Exception as error:
        error.args
