import discord
from discord.ext import commands


@commands.command(name='info')
async def info(ctx):
    """
    await ctx.message.delete()
    db.new_user(ctx.message.author.id,
                ctx.message.author.name + '#' + ctx.message.author.discriminator)
    user = ctx.message.author if not member else member
    dotaid = db.get_dotaid(user.id)
    balance = db.get_balance(user.id)
    souls = db.get_souls(user.id)
    emoji = bot.get_emoji(891212678788431882)

    embed = discord.Embed(
        title=user.name + '#' + user.discriminator,
        # description = f'ID: `{userid}`\nDOTA ID: `{dotaid}`\n\nBALANCE: `{balance}` RUB\nSOULS: `{souls}`\n\nWIN: `{win}`\nLOSE: `{lose}`\nWINRATE: `{winrate}`%',
        # description =  f'**ID:** `{userid}`\n**DOTA ID:** `{dotaid}`\n\n**BALANCE: **`{round(balance, 2)} ₽`\n**SOULS: **`{souls}`\n\n**TIER: **`{tier} ({pts})`',
        # description =  f'DOTA ID: ```{dotaid}```\n\nBalance: `{round(balance, 2)}₽`\nSouls: `{souls}`',
        colour=0x303136  # random_hex_color() # 0x00FFFF
    )

    embed.set_thumbnail(url=user.avatar_url)
    embed.insert_field_at(index=0, name='`DOTAID`', value=f'```{dotaid}```',
                          inline=False)
    embed.insert_field_at(index=1, name='`БАЛАНС`',
                          value=f'```{round(balance, 2)}₽```', inline=True)
    embed.insert_field_at(index=2, name=f'`ДУШИ` {emoji}',
                          value=f'```{souls}```', inline=True)

    embed.set_footer(text=str(user.joined_at.strftime("%d %B %Y %I:%M %p")))
    await ctx.send(embed=embed)
    :param ctx:
    :return:
    """
    await ctx.message.delete()
    embed = discord.Embed(title="pong")
    await ctx.send(embed=embed)


@commands.command(name='dota')
async def dota(ctx, dotaid: int):
    await ctx.message.delete()
    embed = discord.Embed(title="pong")
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
    embed = discord.Embed(title="pong")
    await ctx.send(embed=embed)

