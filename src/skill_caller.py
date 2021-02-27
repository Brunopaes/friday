# -*- coding: utf-8 -*-
import reddit_searcher
import punch_a_clock
import stock_alerts
import cantina_band
import helpers
import morse
import coke
import maps
import meli
import wiki
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
    """Middle function for returning "this is the way!" - mandalorian.

    Parameters
    ----------
    message : telebot.types.Message
        The message object.

    Returns
    -------
    mando: mando.this_is_the_way
        This is the way function.

    """
    return 'This is the way'


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


def return_tweet(message):
    """Middle function for calling tweet package.

    Parameters
    ----------
    message : telebot.types.Message
        The message object.

    Returns
    -------
    msg : str
        Tweet url.

    """
    return stock_alerts.PS5StockAlerts().__call__()


def return_user_alert(message):
    """Middle function for calling user alert package.

    Parameters
    ----------
    message : telebot.types.Message
        The message object.

    Returns
    -------
    msg : str
        User/Chat alert list addition/removal.

    """
    functions = {
        'add me': stock_alerts.add_me,
        'drop me': stock_alerts.drop_me,
    }
    return functions.get(message.text.lower())(message)


def return_reddit(message):
    """Middle function for calling reddit package.

    Parameters
    ----------
    message : telebot.types.Message
        The message object.

    Returns
    -------
    msg : str
        User/Chat alert list addition/removal.

    """
    return reddit_searcher.Reddit(message.text.split('/')[-1]).__call__()


def return_galo_tarsilo(message):
    """Middle function for returning "gaucho" vídeo.

    Parameters
    ----------
    message : telebot.types.Message
        The message object.

    Returns
    -------
    msg : str
        User/Chat alert list addition/removal.

    """
    return 'https://www.youtube.com/watch?v=MVYEwZFixJ8'


def return_cantina_band(message):
    """Middle function for calling cantina band package.

    Parameters
    ----------
    message : telebot.types.Message
        The message object.

    Returns
    -------
    msg : str
        Video url.

    """
    return cantina_band.CantinaBand(message.text.lower()).__call__()


def return_wiki(message):
    """Middle function for calling wiki package.

    Parameters
    ----------
    message : telebot.types.Message
        The message object.

    Returns
    -------
    msg : str
        Video url.

    """
    return wiki.wiki(message.text.lower().split(' '))


def return_geocoding(message):
    """Middle function for calling geocoding package.

    Parameters
    ----------
    message : telebot.types.Message
        The message object.

    Returns
    -------
    msg : str
        Video url.

    """
    return maps.geocoding(' '.join(message.text.lower().split(' ')[1:]))


def return_geodecoding(message):
    """Middle function for calling geodecoding package.

    Parameters
    ----------
    message : telebot.types.Message
        The message object.

    Returns
    -------
    msg : str
        Video url.

    """
    return maps.geodecoding(message.text.lower().split(' ')[1:])


def return_meli(message):
    """Middle function for calling mercado livre package.

    Parameters
    ----------
    message : telebot.types.Message
        The message object.

    Returns
    -------
    msg : str
        Video url.

    """
    return meli.meli(message.text.lower().split(' '))
