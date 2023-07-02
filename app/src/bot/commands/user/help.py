from discord.ext import commands


@commands.command(name='report')
async def report(ctx):
    await ctx.send('всем похуй')
