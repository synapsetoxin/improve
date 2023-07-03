import asyncio
import discord

from discord.ext import commands

from app.src.loader import bot, config, text
from app.src.database.models import Wallets
from app.src.tronscan.methods import fetch


@commands.Cog.listener()
async def on_ready():
    channel_id: int = config['discord']['server']['channels']['deposit']
    channel = bot.get_channel(channel_id)

    while True:
        for wallet in Wallets():
            for transaction in fetch(wallet):
                title = text['tronscan']['alert'].format(
                    name=wallet.name.upper(), amount=transaction.amount)
                embed = discord.Embed(title=title)
                embed.set_image(url=config['discord']['gif']['deposit'])

                allowed_mentions = discord.AllowedMentions(everyone=True)
                await channel.send(text['tronscan']['everyone'],
                                   allowed_mentions=allowed_mentions)
                await channel.send(embed=embed)

        await asyncio.sleep(config['tronscan']['delay'])
