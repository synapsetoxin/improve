import discord

from discord.ext import commands

from app.src.loader import text


@commands.command(name='ban')
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, reason: str = ""):
    await member.ban(reason=reason)
    await ctx.message.delete()
    embed = discord.Embed(
        title=text['ban_alert'].format(user=member.name),
        colour=0x303136
    )
    await ctx.send(embed=embed)


@commands.command(name='gift')
@commands.has_permissions(administrator=True)
async def gift(ctx, member: discord.Member, amount: int = 0):
    """
    Бонусные души дает жоско
    :param ctx:
    :param member:
    :param amount:
    :return:
    """
    pass
