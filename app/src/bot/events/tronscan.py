import asyncio
import discord

from discord.ext import commands
from typing import List

from app.src.loader import bot, config
from app.src.database.models import Wallet, Wallets
from microservice.methods import fetch


@commands.Cog.listener()
async def on_ready():
    channel_id: int = config['discord']['server']['channels']['deposit']
    channel = bot.get_channel(channel_id)

    while True:
        wallets: List[Wallet] = Wallets()
        for wallet in wallets:
            transactions = fetch(wallet)
            for transaction in transactions:
                direction: str = transaction['direction']
                amount: float = transaction['amount']

                if direction == 'in':
                    gif: str = config['discord']['gif']['deposit']
                    title = f'ДЕПОЗИТ ОТ {wallet.name.upper()} НА {amount}$'
                    embed = discord.Embed(title=title)
                    embed.set_image(url=gif)
                    everyone = '@everyone @everyone @everyone'
                    allowed_mentions = discord.AllowedMentions(everyone=True)
                    # await channel.send(everyone, allowed_mentions=allowed_mentions)
                    # await channel.send(embed=embed)
        await asyncio.sleep(config['tronscan']['delay'])
