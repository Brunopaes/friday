# -*- coding: utf-8 -*-
import skill_caller


functions = {
    'this is the way': skill_caller.return_mando,
    'ponto': skill_caller.return_punch_a_clock,
    'eta': skill_caller.return_eta,
    'ps5': skill_caller.return_tweet,
    'add me': skill_caller.return_user_alert,
    'drop me': skill_caller.return_user_alert,
    'va se foder': skill_caller.return_galo_tarsilo,
    'porn': skill_caller.return_cantina_band,
    'bible': skill_caller.return_jagshemash,
}

arg_functions = {
    'morse': skill_caller.return_morse,
    'coke': skill_caller.return_coke,
    'btc': skill_caller.return_btc,
    'porn': skill_caller.return_cantina_band,
    'wiki': skill_caller.return_wiki,
    'ping': skill_caller.return_geocoding,
    'pong': skill_caller.return_geodecoding,
    'ml': skill_caller.return_meli,
    'summon': skill_caller.return_summonizer,
}

media_functions = {
    'r/': skill_caller.return_reddit,
}