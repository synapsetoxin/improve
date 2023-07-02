import discord

from discord.ext import commands
from typing import Union

from app.src.database.models import User


@commands.command(name='info')
async def info(ctx):
    await ctx.message.delete()
    user = User(ctx.message.author.id)
    embed = discord.Embed(
        title=ctx.message.author.name,
        colour=0x303136
    )
    embed.set_thumbnail(url=ctx.message.author.avatar.url)
    embed.insert_field_at(index=0, name='`DOTAID`', value=f'```{user.dotaid}```', inline=False)
    embed.insert_field_at(index=1, name='`ДУШИ`', value=f'```{user.balance}₽```', inline=True)

    embed.set_footer(text=str(ctx.message.author.joined_at.strftime("%d %B %Y %I:%M %p")))
    await ctx.send(embed=embed)


@commands.command(name='dota')
async def dota(ctx, dotaid: Union[int, str]):
    await ctx.message.delete()
    if dotaid.isdigit():
        user = User(ctx.message.author.id)
        user.dotaid = dotaid

    embed = discord.Embed(title="Обновлено")
    await ctx.send(embed=embed)


@commands.command(name='tm')
async def transfer_money(ctx):
    """
    async def dota(ctx):
await ctx.message.delete()
    userid = ctx.message.author.id
    userment = ctx.message.author.mention
    user_balance = db.get_balance(userid)
    if user_balance >= amount and amount >= 1:
        db.top_up_balance(member.id, amount)
        db.top_up_balance(userid, -amount)
        embed = discord.Embed(
            title='Перевод денег.',
            description=f'От: {userment}\nКому: {member.mention}\nСумма: `{amount} RUB`\n\nБаланс {userment}: `{db.get_balance(userid)} RUB`\nБаланс {member.mention}: `{db.get_balance(member.id)} RUB`',
            color=0x303136
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send(
            f'{userment}, у Вас недостаточно средств для перевода. Ваш текущий баланс {user_balance}')

    :param ctx:
    :return:
    """
    await ctx.message.delete()
    embed = discord.Embed(title="Не реализовано")
    await ctx.send(embed=embed)

