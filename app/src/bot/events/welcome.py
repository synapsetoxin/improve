@bot.event
async def on_member_join(member):
    db.new_user(member.id, member.name + '#' + member.discriminator)
    db.top_up_souls(member.id, 2500)
    role = discord.utils.get(member.guild.roles, id=ROLES['noob'])
    channel = bot.get_channel(CHANNELS['door'])
    embed = discord.Embed(
        title='Новый фэриФраер',
        description=member.mention,
        colour=0x00FFFF
    )
    embed.set_thumbnail(url=member.avatar_url)
    await channel.send(embed=embed)
    await member.add_roles(role)

    members_count = member.guild.member_count
    channel = bot.get_channel(STATISTICS['members'])
    await channel.edit(name=f'Users: {members_count}')


@bot.event
async def on_member_remove(member):
    db.top_up_souls(member.id, -2500)
    channel = bot.get_channel(862157697050083379)
    embed = discord.Embed(
        title='Отбыл срок(',
        description=member.mention,
        colour=0x8B0000
    )
    embed.set_thumbnail(url=member.avatar_url)
    await channel.send(embed=embed)

    members_count = member.guild.member_count
    channel = bot.get_channel(STATISTICS['members'])
    await channel.edit(name=f'Users: {members_count}')