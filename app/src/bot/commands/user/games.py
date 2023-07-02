import discord
from discord.ext import commands

from app.src.database.models import User


@commands.command(name='duel')
async def duel(ctx, cost: int):
    # todo: Сделать чтобы по реакции работало
    await ctx.message.delete()
    user = User(ctx.message.author.id)
    if user.balance >= cost >= 1:
        embed = discord.Embed(
            title='Дуэль',
            description=f'Вызвал: {ctx.author.mention}\nСтоимость: `{cost} SOULS`',
            colour=0x303136
        )
        embed.set_footer(text='Нажмите на реакцию, чтобы ответить на дуэль!')
        message = await ctx.send(embed=embed)

        await message.add_reaction(emoji='🎲')
    else:
        await ctx.send(f'{ctx.message.author.mention}, недостаточно средств!')
