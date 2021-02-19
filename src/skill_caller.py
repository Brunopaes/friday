# -*- coding: utf-8 -*-
import punch_a_clock
import helpers
import mando
import morse
import coke
import btc
import eta


def return_punch_a_clock(message):
    """Middle function for calling punch_a_clock package.

    Parameters
    ----------
    message : telebot.types.Message
        The message object.

    Returns
    -------
    pac: punch_a_clock.NexusRPA
        Punch a Clock function.

    """
    helpers.check_user(message.from_user.id)
    return punch_a_clock.NexusRPA().__call__()


def return_eta(message):
    """Middle function for calling return_eta package.

    Parameters
    ----------
    message : telebot.types.Message
        The message object.

    Returns
    -------
    eta: eta.calc_eta
        Eta function.

    """
    return eta.calc_eta()


def return_mando(message):
    """Middle function for calling mando package.

    Parameters
    ----------
    message : telebot.types.Message
        The message object.

    Returns
    -------
    mando: mando.this_is_the_way
        This is the way function.

    """
    return mando.this_is_the_way()


def return_morse(message):
    """Middle function for calling morse package.

    Parameters
    ----------
    message : telebot.types.Message
        The message object.

    Returns
    -------
    morse: morse.morse_parser
        Morse parser function.

    """
    return morse.morse_parser(' '.join(message.text.split(' ')[1:]))


def return_coke(message):
    """Middle function for calling coke package.

    Parameters
    ----------
    message : telebot.types.Message
        The message object.

    Returns
    -------
    coke: coke.coke_function
        Coke functions.

    """
    msg_ = message.text.lower().split(' ')
    coke_functions = {
        'add': coke.insert_coke,
        'check': coke.aggregate,
        'reset': coke.reset,
        'drop': coke.drop
    }

    return coke_functions.get(msg_[1])(message)


def return_btc(message):
    """Middle function for calling btc package.

    Parameters
    ----------
    message : telebot.types.Message
        The message object.

    Returns
    -------
    msg : str
        The BTC api return (buy and sell prices).

    """
    def price(nested_message):
        return btc.BTCoin().__call__()

    def fees(nested_message):
        return btc.Fees(nested_message).__call__()

    def trade(nested_message):
        return btc.Trade(nested_message).__call__()

    msg_ = message.text.lower().split(' ')
    btc_functions = {
        'price': price,
        'fees': fees,
        'trade': trade
    }
    return btc_functions.get(msg_[1])(message)
