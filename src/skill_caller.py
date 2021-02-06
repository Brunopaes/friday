from src import coke, eta, mando, morse, punch_a_clock


def return_punch_a_clock():
    return punch_a_clock.NexusRPA().__call__()


def return_eta():
    return eta.calc_eta()


def return_mando():
    return mando.this_is_the_way()


def return_morse(msg):
    return morse.morse_parser(msg)


def return_coke(milliliters):
    return coke.insert_coke(milliliters)
