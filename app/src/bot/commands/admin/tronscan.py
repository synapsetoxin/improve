import discord

from discord.ext import commands

from app.src.database.models import Wallets, Wallet
from app.src.loader import text


@commands.command(name='wallet')
@commands.has_permissions(administrator=True)
async def wallet(ctx, command: str, address: str, name: str):
    await ctx.message.delete()
    wallets = Wallets()
    _wallet = Wallet(address, name)

    match command:
        case 'add':
            wallets.add(_wallet)
        case 'rename':
            wallets.add(_wallet)
        case 'remove':
            wallets.remove(_wallet)
        case 'list':
            d = '\n'.join(f'{w.name} - {w.address}' for w in wallets)
            embed = discord.Embed(title=text['wallet']['list'], description=d)
            await ctx.send(embed=embed)
        case _:
            await ctx.send(text['wallet']['help'])
