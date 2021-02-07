# -*- coding: utf-8 -*-
import punch_a_clock
import mando
import morse
import coke
import eta


def return_punch_a_clock():
    return punch_a_clock.NexusRPA().__call__()


def return_eta():
    return eta.calc_eta()


def return_mando():
    return mando.this_is_the_way()


def return_morse(msg):
    return morse.morse_parser(msg)


def return_coke(msg):
    msg_ = msg.split(' ')
    coke_functions = {
        'add': coke.insert_coke,
        'check': coke.aggregate
    }

    return coke_functions.get(msg_[0])(msg_[1])
