import discord
from discord.ext import commands


@commands.command(name='adminhelp')
@commands.has_permissions(administrator=True)
async def adminhelp(ctx):
    await ctx.message.delete()
    # embed = discord.Embed(
    #     title='Команды по турниру',
    #     description=yaml['tournament_help'],
    #     colour=0x303136
    # )
    # await ctx.send(embed=embed)
    #
    # embed = discord.Embed(
    #     title='Модерация',
    #     description=yaml['moderation_help'],
    #     colour=0x303136
    # )
    # await ctx.send(embed=embed)
