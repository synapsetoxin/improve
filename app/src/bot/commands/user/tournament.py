import discord

from discord.ext import commands


@commands.command(name='reg')
async def reg(ctx):
    # todo: Выдавать роль zxc
    # todo: Проверять наличие dotaid
    # todo: Проверять балик
    await ctx.message.delete()
    embed = discord.Embed(title="pong")
    embed.set_thumbnail(url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)


@commands.command(name='unreg')
async def unreg(ctx):
    zxcmember = discord.utils.get(ctx.message.author.guild.roles,
                                  id=ROLES['zxcmember'])
    await ctx.message.author.remove_roles(zxcmember)
    embed = discord.Embed(
        title=player + ' отменил регистрацию.',
        colour=0x303136  # random_hex_color()
    )
    embed.set_thumbnail(url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)
    await ctx.message.delete()
    embed = discord.Embed(title="pong")
    await ctx.send(embed=embed)
