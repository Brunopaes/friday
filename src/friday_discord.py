# -*- coding: utf-8 -*-
import skill_caller
import helpers
import discord
import random

friday = discord.Client()


functions = {
    'this is the way': skill_caller.return_mando,
    # 'ponto': skill_caller.return_punch_a_clock,
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
}

media_functions = {
    'r/': skill_caller.return_reddit,
}


@friday.event
async def on_message(message):
    if message.author.id == friday.user.id:
        return

    message_text = message.content.lower().split(' ')
    try:
        if len(message_text) > 1:
            response = arg_functions.get(message_text[0])(message)
        else:
            response = functions.get(message_text[0])(message)
    except TypeError:
        try:
            response = functions.get(message_text[0])(message)
        except AttributeError:
            response = 'Impossible, perhaps the archives are incomplete!'

    await message.channel.send(response)


friday.run(helpers.read_json('settings/discord_settings.json').get('token'))
