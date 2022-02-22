# -*- coding: utf-8 -*-
from discord.ext.commands import Bot

import asyncio
import discord
import helpers
import skills
import io

friday = Bot(command_prefix='')

functions = skills.functions
arg_functions = skills.arg_functions
media_functions = skills.media_functions


@friday.command(
    name='hello there',
    aliases=('Hello', 'hello', 'HELLO', 'HELLO THERE', 'Hello There'),
    description='General Kenobi',
    pass_context=True
)
async def hello_there(context):
    payload = helpers.discord_payload_parser(context)
    if context.message.content.lower() != 'hello there':
        return

    if context.author.voice:
        channel = context.message.author.voice.channel
        voice = await channel.connect()

        voice.play(discord.FFmpegPCMAudio('../data/generalkenobi.mp3'))

        while voice.is_playing():
            await asyncio.sleep(1)

        await voice.disconnect()

    helpers.StoreMetadata(payload).__call__()


@friday.command(
    name='poll',
    description='General Kenobi',
    pass_context=True
)
async def quick_poll(ctx, question, *options: str):
    if len(options) <= 1:
        await ctx.send('You need more than one option to make a poll!')
        return
    if len(options) > 10:
        await ctx.send('You cannot make a poll for more than 10 things!')
        return

    if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
        reactions = ['✅', '❌']
    else:
        reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

    description = []
    for x, option in enumerate(options):
        description += '\n {} {}'.format(reactions[x], option)

    embed = discord.Embed(title=question, description=''.join(description))
    react_message = await ctx.send(embed=embed)

    embed.set_footer(text='Poll ID: {}'.format(react_message.id))
    await react_message.add_reaction("✅")
    await react_message.add_reaction("❌")


@friday.command(
    name='darth plagueis',
    aliases=(
            'darth', 'Darth', 'DARTH',
            'tragedy', 'Tragedy', 'TRAGEDY',
            'tragédia', 'Tragédia', 'TRAGÉDIA',
            'ironic', 'Ironic', 'IRONIC'
    ),
    description='General Kenobi',
    pass_context=True
)
async def darth_plagueis(context):
    payload = helpers.discord_payload_parser(context)
    url = 'https://www.youtube.com/watch?v=05dT34hGRdg'

    if context.author.voice:
        channel = context.message.author.voice.channel
        voice = await channel.connect()

        audio_tuple = helpers.youtube_video_player(url)

        voice.play(discord.FFmpegPCMAudio(
            audio_tuple[0], **audio_tuple[1]
        ))

        while voice.is_playing():
            await asyncio.sleep(1)

        await voice.disconnect()

    helpers.StoreMetadata(payload).__call__()


@friday.event
async def on_message(message):
    await friday.process_commands(message)
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
                if payload.get('message').startswith('r/'):
                    bytes_ = io.BytesIO()

                    image = media_functions.get('r/')(payload)
                    image.save(bytes_, format='png')
                    bytes_.seek(0)

                    d_file = discord.File(bytes_, filename='image.png')

                    response = 'Random submission from {}'.format(
                        payload.get('message')
                    )
                else:
                    response = functions.get(
                        payload.get('message')
                    )(message)
            except Exception as e:
                e.args
                response = None

    if response is None:
        return

    try:
        await message.channel.send(response, file=d_file)
    except discord.errors.HTTPException:
        await message.channel.send(
            'Impossible, perhaps the archives are incomplete!'
        )

    helpers.StoreMetadata(payload).__call__()


friday.run(
    helpers.read_json('settings/discord_settings.json').get('token')
)
