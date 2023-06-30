


@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == MESSAGES['verify']:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
        role = None

        if payload.emoji.name == '💡':
            role = discord.utils.get(guild.roles, id=ROLES['noob'])
        else:
            pass

        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id,
                                        guild.members)
            if member is not None:
                await member.add_roles(role)

    # culture
    elif message_id == 888188138315481098:
        emoji = bot.get_emoji(870057249538736238)
        if payload.emoji == emoji:
            db.top_up_souls(payload.user_id, 3000)

    # shop page scrolling
    elif payload.emoji.name in ['▶️',
                                '◀️'] and payload.user_id != 870051732628078662:
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        await message.remove_reaction(payload.emoji,
                                      bot.get_user(payload.user_id))
        index = int(message.embeds[0].description.splitlines()[0].replace('=',
                                                                          '').replace(
            '*', '').strip())

        count = 1
        result = ''
        emoji = bot.get_emoji(891212678788431882)
        if payload.emoji.name == '▶️':
            index += 5
            shop = db.shoplist(index - 1, index - 1)
        if payload.emoji.name == '◀️':
            if index == 1 or index == 6:
                index = 1
                shop = db.shoplist(0, 5)
            else:
                index -= 5
                shop = db.shoplist(index - 1, index - 1)

        for line in shop:
            try:
                role = discord.utils.get(bot.get_guild(payload.guild_id).roles,
                                         id=line[0])
                seller = bot.get_user(line[5])
                purchase = line[3]
                cost = line[2]
                result += (f'\n\n============ **{index}** =============\n\n'
                           f'Роль: {role.mention}\n'
                           f'Продавец: `{seller}`\n'
                           f'Продано: `{purchase}`\n'
                           f'Стоимость: `{cost}` {emoji}')
                index += 1
                count += 1
                if count >= 6:
                    break
            except Exception as e:
                db.remove_role(line[0])
                print(line)
                print(e)
                continue
        if result != '':
            result += '\n\n```!роль помощь```'
            embed = discord.Embed(
                title='Список ролей на продажу',
                description=result,
                colour=0x303136  # random_hex_color()
            )
            await message.edit(embed=embed)

    # duel
    elif payload.emoji.name == '🎲':
        if payload.user_id != 870051732628078662:
            channel = bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            cost = int(
                message.embeds[0].description.split('Стоимость: ')[1].replace(
                    '`', '').replace('SOULS', ''))
            a_player = bot.get_user(
                int(
                    message.embeds[0].description.split(': ')[1].split()[
                        0].replace('<', '').replace('>', '').replace('@',
                                                                     '').replace(
                        '!', '')
                )
            )
            b_player = bot.get_user(payload.user_id)
            a_balance = float(db.get_souls(a_player.id))
            b_balance = float(db.get_souls(b_player.id))
            if a_balance >= cost and b_balance >= cost:
                players = [a_player, b_player]
                winner = random.choice(players)
                players.remove(winner)
                loser = players[0]
                db.top_up_souls(winner.id, cost)
                db.top_up_souls(loser.id, -cost)
                embed = discord.Embed(
                    title='Итог дуэли!',
                    description=f'Победитель: {winner.mention}\nПроигравший: {loser.mention}\nСтавка: `{cost} SOULS`',
                    color=0x303136
                )
                await message.edit(embed=embed)
                reaction = discord.utils.get(message.reactions,
                                             emoji=payload.emoji.name)
                await reaction.remove(b_player)
                await reaction.remove(bot.get_user(870051732628078662))


@bot.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 888188138315481098:
        emoji = bot.get_emoji(870057249538736238)
        if payload.emoji == emoji:
            db.top_up_souls(payload.user_id, -3000)

