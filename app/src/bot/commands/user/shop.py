import discord

from discord.ext import commands


"""
Личная комната
Стоимость:
• активация: 500 :gold: на 1 месяц
• продление: 1500 :necromastery: за 1 день
• изменение названия: 2000 :necromastery:

Возможности:
• выдача доступа в комнату своим друзьям

Доп. правила:
Название комнаты не должно содержать: оскорбления, рекламу или же нацистскую символику

Команды:
• !рума — примеры команд
• !рума создать <название> — создание комнаты
• !рума продлить <id > <кол-во дней> — продление роли
• !рума + <id> <id / @юзер> — выдать доступ
• !рума - <id> <id / @юзер> — забрать доступ
• !рума инфо <id> — информация о комнате
• !рума доступ <id> — список людей с доступом к комнате

Лаврума
Стоимость:
• активация: 20000 :necromastery: на 1 месяц
• продление: 600 :necromastery: за 1 день

Возможности:
• добавление музыкальных ботов

Команды:
• !лав — примеры команд
• !лав создать <id / @юзер> — создание лавруму
• !лав продлить <кол-во дней> — продление лаврумы
• !лав удалить — удалить лавруму (с возвратом средств)
• !лав инфо — информация о лавруме

"""


@commands.command(name='shop')
async def shop(ctx):
    """
    await ctx.message.delete()
    if action in ['help', 'помощь', 'хелп']:
        embed = discord.Embed(
            title='Личная роль',
            description=yaml['role_shop_help'],
            colour=0x303136  # random_hex_color()
        )
        await ctx.send(embed=embed)

    if action in ['create', 'создать']:
        if a != None and b != None and db.get_souls(ctx.author.id) >= 30000:
            color = int(a.replace("#", ''), 16)
            rolename = ctx.message.content.replace('?', '').replace('!',
                                                                    '').replace(
                'role', '').replace('роль', '').replace('create', '').replace(
                'создать', '').replace(a, '')
            role = await ctx.guild.create_role(name=rolename, color=color,
                                               mentionable=True)
            db.shopcreate(role.id, role,
                          ctx.author.name + '#' + ctx.author.discriminator,
                          ctx.author.id)
            db.top_up_souls(ctx.author.id, -30000)
            await ctx.message.author.add_roles(role)
            embed = discord.Embed(
                title='Создана новая роль',
                description=f'Роль: {role.mention}\nСоздатель: {ctx.author.mention}\nДействительна до: `{db.role_expire(role.id)}`',
                colour=color
            )
            embed.set_thumbnail(url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send('У Вас недостаточно душ')

    if action in [None, 'магазин', 'shop']:
        result = ''
        index = 1
        shop = db.shoplist(0, 5)  # .splitlines()
        emoji = bot.get_emoji(891212678788431882)
        for line in shop:
            try:
                role = discord.utils.get(ctx.message.author.guild.roles,
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
            except Exception as e:
                continue
        result += '\n\n```!роль помощь```'
        embed = discord.Embed(
            title='Список ролей на продажу',
            description=result,
            colour=0x303136  # random_hex_color()
        )
        # await ctx.send(embed=embed)
        message = await ctx.send(embed=embed)
        await message.add_reaction(emoji='◀️')
        await message.add_reaction(emoji='▶️')

    if action in ['extend', 'продлить']:
        extend_cost = db.get_settings('role_extend')
        days_extend = int(b)
        role_id = int(a[3:-1])
        role = discord.utils.get(ctx.message.author.guild.roles, id=role_id)
        souls_cost = days_extend * extend_cost
        user_souls = db.get_souls(ctx.message.author.id)
        if souls_cost < user_souls:
            expire = db.role_expire(role_id)
            year = int(expire.split('-')[2])
            mounth = int(expire.split('-')[1])
            day = int(expire.split('-')[0])
            _new_expire = dt(year, mounth, day) + timedelta(days_extend)
            _new_expire_split = str(_new_expire).split()[0]
            _nes = _new_expire_split.split('-')
            new_expire = _nes[2] + '-' + _nes[1] + '-' + _nes[0]
            db.role_extend(role_id, new_expire)
            db.top_up_souls(ctx.message.author.id, -souls_cost)
            await ctx.send(f'{role} продлена на {days_extend} дней!')
        else:
            await ctx.send('У Вас недостаточно душ')

    if action in ['color', 'цвет']:
        role = discord.utils.get(ctx.message.author.guild.roles,
                                 id=int(a[3:-1]))
        if db.role_owner(role.id, ctx.message.author.id):
            color = int(b.replace("#", ''), 16)
            # await bot.edit_role(server=server, role=role, colour=discord.Colour(colours[i]))
            if db.get_souls(ctx.message.author.id) >= 2000:
                db.top_up_souls(ctx.message.author.id, -2000)
                await role.edit(color=color)
                await ctx.send('Цвет роли изменен.')
            else:
                await ctx.send('Недостаточно душ. Требуется 2000.')
        else:
            await ctx.send('У Вас нет прав менять эту роль.')

    if action in ['name', 'имя']:
        pass

    if action == '+':
        pass

    if action == '-':
        pass

    if action in ['info', 'инфо']:
        role = discord.utils.get(ctx.message.author.guild.roles,
                                 id=int(a[3:-1]))
        if db.role_sale_exist(role.id):
            embed = discord.Embed(
                title=f'{role.name}',
                description=f'**Продавец: **`{db.role_seller(role.id)}`\n**Стоимость: **`{db.role_cost(role.id)} душ`\n**Продано: **`{db.role_purchase(role.id)}`\n**Действительна до: **`{db.role_expire(role.id)}`',
                colour=role.color
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(
                f'{ctx.message.author.mention}, данной роли нет в продаже.')

    if action in ['продажа', 'sale']:
        db.set_role_sale(int(a[3:-1]))
        if db.role_sale_exist(int(a[3:-1])):
            await ctx.send('Роль добавлена на продажу')
        else:
            await ctx.send('Роль убрана с продажи')

    if action in ['price', 'цена']:
        role = discord.utils.get(ctx.message.author.guild.roles,
                                 id=int(a[3:-1]))
        cost = b
        db.set_role_cost(role.id, cost)
        await ctx.send('Цена выставлена.')

    if action in ['buy', 'купить']:
        role = discord.utils.get(ctx.message.author.guild.roles,
                                 id=int(a[3:-1]))
        userid = ctx.message.author.id
        role_cost = db.role_cost(role.id)
        if role not in ctx.message.author.roles:
            if role_cost <= db.get_souls(userid):
                db.top_up_souls(userid, -role_cost)
                db.add_role_purchase(role.id)
                db.top_up_souls(db.role_seller_id(role.id), role_cost)
                await ctx.message.author.add_roles(role)
                await ctx.send(
                    f'{ctx.message.author.mention} приобрел роль {role.mention}')
            else:
                await ctx.send(
                    f'{ctx.message.author.mention}, у Вас недостаточно душ.')
        else:
            await ctx.send(
                f'{ctx.message.author.mention}, у Вас уже есть эта роль!')

    if action in ['remove', 'удалить']:
        role = discord.utils.get(ctx.message.author.guild.roles,
                                 id=int(a[3:-1]))
        if db.role_owner(role.id, ctx.author.id):
            await role.delete()
            db.remove_role(int(a[3:-1]))
            await ctx.send('Роль удалена')
    :param ctx:
    :return:
    """
    await ctx.message.delete()
    embed = discord.Embed(title="Не реализовано")
    await ctx.send(embed=embed)
