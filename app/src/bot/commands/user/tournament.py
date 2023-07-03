import discord

from discord.ext import commands

from app.src.database.models import User
from app.src.loader import text, config


@commands.command(name='reg')
async def reg(ctx):
    # todo: Выдавать роль zxc
    # todo: Проверять балик
    await ctx.message.delete()
    user = User(ctx.message.author.id)
    role = None  # config['discord']['server']['role']['zxc']
    if user.dotaid:
        pass
    else:
        await ctx.send(text['tournament']['reg']['error'])
    embed = discord.Embed(title="Не реализовано")
    # embed.set_thumbnail(url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)


@commands.command(name='unreg')
async def unreg(ctx):
    # zxcmember = discord.utils.get(ctx.message.author.guild.roles,
    #                               id=ROLES['zxcmember'])
    # await ctx.message.author.remove_roles(zxcmember)
    # embed = discord.Embed(
    #     title=player + ' отменил регистрацию.',
    #     colour=0x303136  # random_hex_color()
    # )
    # embed.set_thumbnail(url=ctx.message.author.avatar_url)
    # await ctx.send(embed=embed)
    await ctx.message.delete()
    embed = discord.Embed(title="Не реализовано")
    await ctx.send(embed=embed)
