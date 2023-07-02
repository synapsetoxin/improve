import discord
from discord.ext import commands

from app.src.database.models import Wallets, Wallet


@commands.command(name='wallet')
@commands.has_permissions(administrator=True)
async def wallet(ctx, address: str, name: str):
    await ctx.message.delete()
    Wallets().add(Wallet(address, name))
    await ctx.send(f"Добавлен кошелек!\nИмя: {wallet.name}\nАдрес:{wallet.address}")  # todo: make in yaml
