@bot.command()
async def report(ctx):
    await ctx.send('всем похуй')


@bot.command(aliases=['помощь', 'хелп'])
async def help(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title='Команды',
        description=yaml['help'],
        colour=0x303136  # random_hex_color()
    )
    await ctx.send(embed=embed)