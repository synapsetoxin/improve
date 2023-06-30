import discord
from discord.ext import commands


@commands.command(name='duel')
async def duel(ctx):
    await ctx.message.delete()
    if db.get_souls(ctx.message.author.id) >= cost and cost >= 1:
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
