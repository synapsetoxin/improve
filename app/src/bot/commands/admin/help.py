

@bot.command()
@commands.has_permissions(administrator=True)
async def adminhelp(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title='Команды по турниру',
        description=yaml['tournament_help'],
        colour=0x303136
    )
    await ctx.send(embed=embed)

    embed = discord.Embed(
        title='Модерация',
        description=yaml['moderation_help'],
        colour=0x303136
    )
    await ctx.send(embed=embed)

    embed = discord.Embed(
        title='Финансы',
        description=yaml['finance_help'],
        colour=0x303136
    )
    await ctx.send(embed=embed)

    embed = discord.Embed(
        title='Коуч',
        description=yaml['coach_moderation_help'],
        colour=0x303136
    )
    await ctx.send(embed=embed)