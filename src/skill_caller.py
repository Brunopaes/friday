# -*- coding: utf-8 -*-
import punch_a_clock
import mando
import morse
import coke
import btc
import eta


def return_punch_a_clock():
    """Middle function for calling punch_a_clock package.

    Returns
    -------
    pac: punch_a_clock.NexusRPA
        Punch a Clock function.

    """
    return punch_a_clock.NexusRPA().__call__()


def return_eta():
    """Middle function for calling return_eta package.

    Returns
    -------
    eta: eta.calc_eta
        Eta function.

    """
    return eta.calc_eta()


def return_mando():
    """Middle function for calling mando package.

    Returns
    -------
    mando: mando.this_is_the_way
        This is the way function.

    """
    return mando.this_is_the_way()


def return_morse(msg):
    """Middle function for calling morse package.

    Returns
    -------
    morse: morse.morse_parser
        Morse parser function.

    """
    return morse.morse_parser(msg)


def return_coke(msg):
    """Middle function for calling coke package.

    Returns
    -------
    coke: coke.coke_function
        Coke functions.

    """
    msg_ = msg.split(' ')
    coke_functions = {
        'add': coke.insert_coke,
        'check': coke.aggregate,
        'drop': coke.drop
    }

    return coke_functions.get(msg_[0])(msg_[-1])


def return_btc():
    """Middle function for calling btc package.

    Returns
    -------
    msg : str
        The BTC api return (buy and sell prices).

    """
    return btc.BTCoin().__call__()
