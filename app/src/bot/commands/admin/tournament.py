import discord

from discord.ext import commands


@commands.command(name='ct')
@commands.has_permissions(administrator=True)
async def create_tournament(ctx):
    """
    Create tournament
    todo: Нужно создать роль zxc которая будет выдаваться участникам
     и удаляться при отмене турнира + возврат бабок при отмене
    todo: Если не указан прайс, то цена 0, проверять темку надо
    :param ctx:
    :return:
    """
    await ctx.message.delete()
    embed = discord.Embed(title="pong")
    await ctx.send(embed=embed)


@commands.command(name='rt')
@commands.has_permissions(administrator=True)
async def remove_tournament(ctx):
    """
    Remove tournament
    :param ctx:
    :return:
    """
    role = discord.utils.get(ctx.message.author.guild.roles,
                             id=ROLES['zxcmember'])
    for member in role.members:
        await member.remove_roles(role)
    await ctx.message.delete()
    embed = discord.Embed(title="pong")
    await ctx.send(embed=embed)


@commands.command(name='rt')
@commands.has_permissions(administrator=True)
async def remove_tournament(ctx):
    """
    Remove tournament
    :param ctx:
    :return:
    """
    role = discord.utils.get(ctx.message.author.guild.roles,
                             id=ROLES['zxcmember'])
    for member in role.members:
        await member.remove_roles(role)
    await ctx.message.delete()
    embed = discord.Embed(title="pong")
    await ctx.send(embed=embed)


@commands.command(name='reglist')
@commands.has_permissions(administrator=True)
async def reglist(ctx):
    """
    Reglist
    :param ctx:
    :return:
    """
    await ctx.message.delete()
    embed = discord.Embed(title="pong")
    await ctx.send(embed=embed)
