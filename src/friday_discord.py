# -*- coding: utf-8 -*-
import helpers
import discord
import skills
import io

friday = discord.Client()

functions = skills.functions
arg_functions = skills.arg_functions
media_functions = skills.media_functions


@friday.event
async def on_message(message):
    if message.author.id == friday.user.id:
        return

    d_file = None
    payload = helpers.discord_payload_parser(message)
    message_text = payload.get('message').lower().split(' ')
    try:
        if len(message_text) > 1:
            response = arg_functions.get(message_text[0])(payload)
        else:
            response = functions.get(message_text[0])(payload)
    except TypeError:
        try:
            response = functions.get(message_text[0])(payload)
        except TypeError:
            try:
                bytes_ = io.BytesIO()

                image = media_functions.get('r/')(payload)
                image.save(bytes_, format='png')
                bytes_.seek(0)

                d_file = discord.File(bytes_, filename='image.png')

                response = 'Random submission from {}'.format(
                    payload.get('message')
                )
            except Exception as e:
                e.args
                response = \
                    'Impossible, perhaps the archives are incomplete!'

    await message.channel.send(response, file=d_file)


friday.run(
    helpers.read_json('settings/discord_settings.json').get('token')
)
