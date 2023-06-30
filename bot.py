# coding: utf-8

import discord
from discord.ext import commands 
from discord import NotFound
from discord_components import DiscordComponents, Button, ButtonStyle
import configparser
import yaml
from asyncio import sleep
from database import Database as db
import random
import asyncio
import time
import re
import datetime
from datetime import datetime as dt
from datetime import timedelta
from typing import Union
import json
import requests


with open('yaml.yaml', 'r', encoding="utf8") as file:
	yaml = yaml.safe_load(file)

config = configparser.ConfigParser()
config.read('config.ini')


TOKEN = config['bot']['TOKEN']
SERVER_ID = 862136834447114290
CHANNELS = {
	'door': 862157697050083379,
	'create-voice-channel': 886299297325408337,
	'roulette': 891361073805013043,
	'withdraw': 899964223369642015
}
CATEGORIES = {
	'private-voice': 870066272216424478
}
ROLES = {
	'voicemute':  870648493407105045, 
	'chatmute':   870648973847834655,
	'noob':       870623936960938035,
	'zxcmember':  864460160063635476,
	'test': 	  872989338684768316,
	'boost':      863361128439349289,
	'admin':      862139993698074674,
	'clown':      872869000558809138
}
MESSAGES = {
	'verify': 876219033249259530
}
STATISTICS = {
	'members': 889966914347106325,
	'voice': 889971317967839232
}


bot = commands.Bot(command_prefix = ['?', '!', '/'], intents = discord.Intents.all())
client = discord.Client()
bot.remove_command('help')


def random_hex_color():
	rgb = ""
	for _ in "RGB":
		i = random.randrange(0, 256)
		rgb += i.to_bytes(1, "big").hex()
	return int(rgb, 16)

@bot.command()
async def report(ctx):
	await ctx.send('всем похуй')

@bot.command()
async def test(ctx, *args):
    retStr = str("""```css\nThis is some colored Text```""")
    embed = discord.Embed(title="Random test")
    embed.add_field(name="Name field can't be colored as it seems",value=retStr)
    await ctx.send(embed=embed)

# @bot.command()
# async def test(ctx):
# 	embed = discord.Embed(
# 		title = 'text', 
# 		description = '''```css
# green text
# ```'''
# 		)

# 	message = await ctx.send(
# 		embed=embed,
# 		components = [
# 			Button(style=ButtonStyle.red, label='кнопка', emoji = '🎰')
# 			]
# 		)
# 	response = await bot.wait_for('button_click')
# 	if response.channel == ctx.channel:
# 		if response.component.label == 'кнопка':
# 			print(message.embeds[0].description)
# 			await response.respond(content = 'button clicked')


# @bot.command(name="test")
# async def test(ctx): # waiting for reactions (✅, ❌) here
#     await ctx.send(f"**{ctx.author}**, please react with :white_check_mark: or :x: on this message in 60 seconds")
	
#     def check(r: discord.Reaction, u: Union[discord.Member, discord.User]):  # r = discord.Reaction, u = discord.Member or discord.User.
#         return u.id == ctx.author.id and r.message.channel.id == ctx.channel.id and \
#                str(r.emoji) in ["\U00002705", "\U0000274c"]
#         # checking author, channel and only having the check become True when detecting a ✅ or ❌
#         # else, it will timeout.

#     try:
#         #                                   event = on_reaction_add without on_
#         reaction, user = await bot.wait_for(event = 'reaction_add', check = check, timeout = 60.0)
#         # reaction = discord.Reaction, user = discord.Member or discord.User.
#     except asyncio.TimeoutError:
#         # at this point, the check didn't become True.
#         await ctx.send(f"**{ctx.author}**, you didnt react with a ✅ or ❌ in 60 seconds.")
#         return
#     else:
#         # at this point, the check has become True and the wait_for has done its work, now we can do ours.
#         # here we are sending some text based on the reaction we detected.
		
#         #                         unicode for ✅ :
#         #                         https://emojipedia.org/emoji/✅/#:~:text=Codepoints
#         if str(reaction.emoji) == "\U00002705":
#             return await ctx.send(f"{ctx.author} reacted with a ✅")
#             # or we could also add a role here, like so
#             # role = await ctx.guild.get_role(ROLE_ID)
#             # await ctx.author.add_roles(role)
			
#         #                         unicode for ❌ :
#         #                         https://emojipedia.org/emoji/❌/#:~:text=Codepoints
#         if str(reaction.emoji) == "\U0000274c":
#             return await ctx.send(f"{ctx.author} reacted with a ❌")


@bot.command(aliases=['помощь', 'хелп'])
async def help(ctx):
	await ctx.message.delete()
	embed = discord.Embed(
		title = 'Команды',
		description = yaml['help'],
		colour = 0x303136 # random_hex_color()
		)
	await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def adminhelp(ctx):
	await ctx.message.delete()
	embed = discord.Embed(
		title = 'Команды по турниру',
		description = yaml['tournament_help'],
		colour = 0x303136 
		)
	await ctx.send(embed=embed)
	
	embed = discord.Embed(
		title = 'Модерация',
		description = yaml['moderation_help'],
		colour = 0x303136
		)
	await ctx.send(embed=embed)

	embed = discord.Embed(
		title = 'Финансы',
		description = yaml['finance_help'],
		colour = 0x303136
		)
	await ctx.send(embed=embed)

	embed = discord.Embed(
		title = 'Коуч',
		description = yaml['coach_moderation_help'],
		colour = 0x303136
		)
	await ctx.send(embed=embed)


# MODERATION


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, reason=None):
	await member.ban(reason=reason)
	await ctx.message.delete()
	embed = discord.Embed(
		title=yaml['ban_alert'].format(user = member.name.mention), 
		colour=0x303136
		)
	await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member=None, tm='infinite', reason='не указана'):
	if not member:
		await ctx.message.delete()
		ctx.send(yaml['specify_user'])
	else:
		await ctx.message.delete()
		member_nick = member.nick if member.nick != None else member.name
		role = discord.utils.get(ctx.message.guild.roles, id=ROLES['chatmute'])
		replaces = ['?', '!', 'chatmute', tm, member.mention]
		reason = ctx.message.content if ctx.message.content != '' else 'не указана'
		print(ctx.message.author, 'muted', member)
		for r in replaces:
			reason = reason.replace(r, '')
		if tm == 'infinite':
			mute = discord.Embed(
				title = 'Mute', 
				description = yaml['infinite_chat_mute_alert'].format(
					user = member_nick,
					admin = ctx.author.mention,
					reason = reason
					),
				color = 0x303136
				)
			await member.add_roles(role)
			await ctx.send(embed=mute)
		else:
			mute = discord.Embed(
				title = 'Mute', 
				description = yaml['chat_mute_alert'].format(
					user = member_nick,
					time = tm,
					admin = ctx.author,
					reason = reason),
				color = 0x303136
				)
			unmute = discord.Embed(
				title = 'UnMute', 
				description = yaml['chat_unmute_alert'].format(user = member_nick),
				color = 0x303136
				)
			await member.add_roles(role)
			await ctx.send(embed=mute)
			await asyncio.sleep(int(tm) * 60)
			await member.remove_roles(role)
			await ctx.send(embed=unmute)


@bot.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member=None):
	await ctx.message.delete()
	if not member:
		ctx.send(yaml['specify_user'])
	else:
		embed = discord.Embed(
			title = 'Unmute', 
			description = yaml['umute_alert'].format(
				user = member.nick if member.nick != None else member.name, 
				admin = ctx.author.mention),
			color = 0x303136
			)
		roles = [
			discord.utils.get(ctx.message.author.guild.roles, id=ROLES['voicemute']),
			discord.utils.get(ctx.message.author.guild.roles, id=ROLES['chatmute'])
		]
		for role in roles:
			try:
				await member.remove_roles(role)
			except:
				continue
		await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def post(ctx):
	await ctx.message.delete()
	text = ctx.message.content.replace('!post', '').replace('?post', '')
	embed = discord.Embed(
		title = text.split('|')[0],
		description = text.split('|')[1],
		colour = 0x303136
		)
	await ctx.send(embed=embed)


@bot.command(aliases=['инфо', 'profile', 'профиль', 'balance', 'баланс'])
async def info(ctx, member: discord.Member=None):
	await ctx.message.delete()
	db.new_user(ctx.message.author.id, ctx.message.author.name + '#' +ctx.message.author.discriminator)
	user = ctx.message.author if not member else member
	dotaid = db.get_dotaid(user.id)
	balance = db.get_balance(user.id)
	souls = db.get_souls(user.id)
	emoji = bot.get_emoji(891212678788431882)

	# tier, pts = db.get_tier_and_pts(user.id)
	# win = db.get_wins(_userid)
	# lose = db.get_loses(_userid)
	# try:
	# 	if lose == 0 and win > 0:
	# 		winrate = 100
	# 	else:
	# 		winrate = round( (win / (win + lose) ) * 100, 1)
	# except:
	# 	winrate = 0

	embed = discord.Embed(
		title = user.name + '#' + user.discriminator,
		# description = f'ID: `{userid}`\nDOTA ID: `{dotaid}`\n\nBALANCE: `{balance}` RUB\nSOULS: `{souls}`\n\nWIN: `{win}`\nLOSE: `{lose}`\nWINRATE: `{winrate}`%',
		# description =  f'**ID:** `{userid}`\n**DOTA ID:** `{dotaid}`\n\n**BALANCE: **`{round(balance, 2)} ₽`\n**SOULS: **`{souls}`\n\n**TIER: **`{tier} ({pts})`',
		# description =  f'DOTA ID: ```{dotaid}```\n\nBalance: `{round(balance, 2)}₽`\nSouls: `{souls}`',
		colour = 0x303136 # random_hex_color() # 0x00FFFF
		)

	# embed.add_field(name='WIN', value=f'`{win}`', inline=True)
	# embed.add_field(name='LOSE', value=f'`{lose}`', inline=True)
	# embed.add_field(name='WINRATE', value=f'`{winrate}%`', inline=True)
	# embed.set_author(
	# 	name = user.name + '#' + user.discriminator,
	# 	icon_url = user.avatar_url)

	embed.set_thumbnail(url=user.avatar_url)
	embed.insert_field_at(index = 0, name = '`DOTAID`', value = f'```{dotaid}```', inline = False)
	embed.insert_field_at(index = 1, name = '`БАЛАНС`', value = f'```{round(balance, 2)}₽```', inline = True)
	embed.insert_field_at(index = 2, name = f'`ДУШИ` {emoji}', value = f'```{souls}```', inline = True)
	
	if db.coacher_exist(user.id):
		tier = db.get_coach_tier(user.id)
		cost = db.get_coach_cost(user.id)
		rate = db.get_coach_rate(user.id)
		embed.insert_field_at(index = 3, name = f'`КОУЧ`', value = f'```Tier: {tier} | {cost} ₽ | {rate}☆```', inline = False)
	
	if db.guarantee_exist(user.id):
		percent = db.get_guarantee_percent(user.id)
		embed.insert_field_at(index = 4, name = f'`ГАРАНТ`', value = f'```Стоимость: {percent}% | Сделок: {0} | {0}☆\n{db.bank_list(user.id)}```', inline = False)

	embed.set_footer(text = str(user.joined_at.strftime("%d %B %Y %I:%M %p")))
	await ctx.send(embed=embed)


@bot.command(aliases=['дота', 'dotaid'])
async def dota(ctx, number=None):
	await ctx.message.delete()
	if number.isdigit() == True:
		db.set_dotaid(ctx.message.author.id, number)
		embed = discord.Embed(
			description = f'```{number}```',
			colour = 0x303136
			)
		embed.set_author(
			name = ctx.message.author.name + '#' + ctx.message.author.discriminator,
			icon_url = ctx.message.author.avatar_url
			)
		await ctx.send(embed=embed)
	else:
		await ctx.send(f'```{number} - Incorrect ID.```')


@bot.command(aliases=['wd'])
async def withdraw(ctx, bank=None, number=None, amount=None):
	await ctx.message.delete()
	withdraw_channel = bot.get_channel(CHANNELS['withdraw'])
	if None not in [bank, number, amount]:
		if int(amount) <= db.get_balance(ctx.message.author.id):
			db.top_up_balance(ctx.message.author.id, int(amount) * -1)
			player = ctx.message.author.name + '#' + ctx.message.author.discriminator
			embed = discord.Embed(
				title = 'Вывод денег',
				description = f'Пользователь: {player}\nБанк: `{bank.upper()}`\nНомер: `{number}`\nКоличество: `{amount} RUB`',
				colour = 0x303136
				)
			await withdraw_channel.send(embed=embed)
			await ctx.send('Запрос принят!')
		else:
			await ctx.send('Недостаточно средств!')
	else:
		await ctx.send('Что-то не указано')

# TOURNAMENT


@bot.command(aliases=['рег', 'регистрация'])
async def reg(ctx):
	await ctx.message.delete()
	player = ctx.message.author.name + '#' + ctx.message.author.discriminator
	db.new_user(ctx.message.author.id, player)
	dotaid = db.get_dotaid(ctx.message.author.id)
	zxcmember = discord.utils.get(ctx.message.author.guild.roles, id=ROLES['zxcmember'])
	boost = discord.utils.get(ctx.message.author.guild.roles, id=ROLES['boost'])
	multiplier = 1
	if boost in ctx.author.roles:
		multiplier = 1.5

	if dotaid == None:
		embed = discord.Embed(
			title = 'Ошибка',
			description = f'{ctx.message.author.mention} не имеет `DOTAID`\n```!dota 123456789```',
			colour = 0x303136 
			)
		embed.set_thumbnail(url=ctx.message.author.avatar_url)
		await ctx.send(embed=embed)

	else:
		tour_cost = int(db.get_tour_cost())
		if db.get_balance(ctx.message.author.id) >= tour_cost:
			db.tournament_registration(player, dotaid)
			db.top_up_balance(ctx.message.author.id, -tour_cost)
			if tour_cost > 0:
				db.top_up_souls(ctx.message.author.id, 1500 * multiplier)
			else:
				db.top_up_souls(ctx.message.author.id, 500 * multiplier)
			await ctx.message.author.add_roles(zxcmember)
			embed = discord.Embed(
				title = 'Новый участник ' + player,
				colour = 0x303136 
				)
			embed.insert_field_at(index = 1, name = '`DOTAID`', value = f'```{dotaid}```', inline = False)
			embed.set_thumbnail(url=ctx.message.author.avatar_url)
			await ctx.send(embed=embed)
		else:
			embed = discord.Embed(
				title = 'Недостаточно средств!',
				description = f'{ctx.message.author.mention} не имеет достаточный баланс.\nЧтобы пополнить баланс на сервере обратитесь к ucantstopme#0690',
				colour = 0x303136 # random_hex_color()
				)
			embed.set_thumbnail(url=ctx.message.author.avatar_url)
			await ctx.send(embed=embed)
			return


@bot.command(aliases=['анрег'])
async def unreg(ctx):
	await ctx.message.delete()
	player = ctx.message.author.name + '#' + ctx.message.author.discriminator
	zxcmember = discord.utils.get(ctx.message.author.guild.roles, id=ROLES['zxcmember'])
	boost = discord.utils.get(ctx.message.author.guild.roles, id=ROLES['boost'])
	multiplier = 1
	if boost in ctx.author.roles:
		multiplier = 1.5

	if db.user_tournament_registered(player):
		db.tournament_unregistration(player)
		tour_cost = int(db.get_tour_cost())
		if tour_cost > 0:
			db.top_up_souls(ctx.message.author.id, -1500 * multiplier)
		else:
			db.top_up_souls(ctx.message.author.id, -500 * multiplier)
		db.top_up_balance(ctx.message.author.id, tour_cost)
		await ctx.message.author.remove_roles(zxcmember)
		embed = discord.Embed(
			title = player + ' отменил регистрацию.',
			colour = 0x303136 # random_hex_color()
			)
		embed.set_thumbnail(url=ctx.message.author.avatar_url)
		await ctx.send(embed=embed)


@bot.command(aliases=['ct'])
@commands.has_role('tournament maker')
async def create_tournament(ctx, cost: int=None):
	await ctx.message.delete()
	try:
		if cost == None:
			db.set_tour_cost(0)
			db.create_tournament()
			await ctx.send('Турнир создан.')
		else:
			db.set_tour_cost(cost)
			db.create_tournament()
			await ctx.send(f'Турнир создан. Стоимость: {cost}')
	except:
		await ctx.send('Турнир уже создан')


@bot.command()
@commands.has_role('tournament maker')
async def cancel_tournament(ctx):
	await ctx.message.delete()
	try:
		tour_cost = db.get_tour_cost()
		players = db.reglist()
		for player in players.splitlines():
			user_id = db.get_userid_from_dotaid(player.split()[1])
			db.top_up_balance(user_id, tour_cost)
		await ctx.send('Всем участникам возвращены деньги на баланс')
		
		db.remove_tournament()
		await ctx.send('Турнир удален.')

		role = discord.utils.get(ctx.message.author.guild.roles, id=ROLES['zxcmember'])
		for member in role.members:
			await member.remove_roles(role)
		await ctx.send('Роль zxc member убрана у пользователей')
		tour_cost = 0
	except:
		await ctx.send('В данный момент турниры не проводятся.')


@bot.command(aliases=['rt'])
@commands.has_role('tournament maker')
async def remove_tournament(ctx):
	await ctx.message.delete()
	try:
		db.set_tour_cost(0)
		db.remove_tournament()
		await ctx.send('Турнир удален.')
		role = discord.utils.get(ctx.message.author.guild.roles, id=ROLES['zxcmember'])
		for member in role.members:
			await member.remove_roles(role)
		await ctx.send('Роль zxc member убрана у пользователей')
	except:
		await ctx.send('В данный момент турниры не проводятся.')


@bot.command()
@commands.has_permissions(administrator=True)
async def rzxc(ctx):
	role = discord.utils.get(ctx.message.author.guild.roles, id=ROLES['zxcmember'])
	for member in role.members:
		await member.remove_roles(role)
	await ctx.send('Роль zxc member убрана у пользователей')


@bot.command()
async def reglist(ctx):
	await ctx.message.delete()
	try:
		players = db.reglist()
		_players = players.replace("'", '').replace(',', '').strip()
		players = ''
		for p in _players.splitlines():
			players += p.strip() + '\n'
		count_player = int(db.count_tournament_players())
		if count_player != 0:
			ticket = db.get_tour_cost()
			if ticket != 0:
				prize = ticket * count_player * 0.9
				embed = discord.Embed(
					title = 'Участники турнира' + f' ({count_player})',
					description = f'**Призовой**: {prize} RUB\n**1st:** {prize * 0.6} (60%)\n**2nd:** {prize * 0.3} (30%)\n**3rd:** {prize * 0.1} (10%)\n```{players.strip()}```',
					colour =  0x303136 # random_hex_color()
					)
				embed.set_footer(text = f'Стоимость входа: {ticket} RUB')
				await ctx.send(embed=embed)
			embed = discord.Embed(
				title = 'Участники турнира' + f' ({count_player})',
				description = f'```{players.strip()}```',
				colour =  0x303136 # random_hex_color()
				)
			await ctx.send(embed=embed)
		else:
			await ctx.send('Участников нет.')
	except:
		await ctx.send('В данный момент турниры не проводятся.')


@bot.command()
@commands.has_permissions(administrator=True)
async def shuffle(ctx):
	await ctx.message.delete()
	players = db.reglist()
	players = players.replace("'", '').replace(',', '')
	players_count = len(players.splitlines()) 
	while players_count % 10 != 0 and players_count % 5 != 0:
		players_count -= 1
	members = []
	for player in players.splitlines():
		members.append(player)
		if len(members) == players_count:
			break
	team_count = len(members) / 5
	teams = []
	for x in range(int(team_count)):
		team = []
		for z in range(5):
			players_count -= 1
			member_random = random.randint(0, players_count)
			team.append(members[member_random])
			del members[member_random]
		teams.append(team)

	x = 1
	result = ''
	for team in teams:
		result += f"\n\n**Команда: {x} **"
		x += 1
		for member in team:
			result += f'\n{member.strip()}'

	await ctx.send(result)


@bot.command()
@commands.has_permissions(administrator=True)
async def tub(ctx, member: discord.Member=None, amount: float=None):
	await ctx.message.delete()

	if amount == None or member == None:
		await ctx.send('Укажите количество или пользователя.\n?tub `user` `amount`')
	else:
		db.top_up_balance(member.id, amount)
		embed = discord.Embed(
			title = 'Баланс изменен (RUB)',
			description = 'Пользователь: ' + member.mention,
			colour =  0x303136 # random_hex_color()
			)
		embed.add_field(name='ДО', value=f'`{db.get_balance(member.id) - amount}`', inline=True)
		embed.add_field(name='ПОСЛЕ', value=f'`{db.get_balance(member.id)}`', inline=True)
		await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def twitch(ctx, url: str=None):
	pass


# РЕЙТИНГОВАЯ СИСТЕМА 

def player_selection():
	players = db.get_lobby_players()
	for player in players:
		print(player)

@bot.command(aliases=['лобби', 'zxc'])
async def lobby(ctx):
	await ctx.message.delete()
	db.toggle_lobby_search(ctx.message.author.id)
	status = db.get_lobby_status(ctx.message.author.id)
	if status == 1:
		tier, pts = db.get_tier_and_pts(ctx.message.author.id)
		games = db.count_lobby_games(ctx.message.author.id)
		user_search = db.get_users_search_lobby()
		win = db.get_wins(ctx.message.author.id)
		lose = db.get_loses(ctx.message.author.id)
		try:
			if lose == 0 and win > 0:
				winrate = 100
			else:
				winrate = round( (win / (win + lose) ) * 100, 1)
		except:
			winrate = 0
		description = f'```Tier: {tier} ({pts})\nИгр: {games}\nВинрейт: {winrate}%```'
		embed = discord.Embed(
			title = 'Поиск лобби...',
			description = description,
			colour =  0x303136
			)
		embed.set_author(
			name = ctx.message.author.name + '#' + ctx.message.author.discriminator,
			icon_url = ctx.message.author.avatar_url
		)
		embed.set_footer(text = f'Игроков в поиске: {user_search}')
		await ctx.send(embed=embed)
	if status == 0:
		await ctx.send('отмена поиска игр')

"""
db.top_up_souls(ctx.message.author.id, 250 * multiplier)
db.set_bump_datetime(ctx.message.author.id, now + 14400)

emoji = bot.get_emoji(891212678788431882)
embed = discord.Embed(
	title = 'Бонус',
	description = f'Вы получили **250** {emoji}\nСледующий бонус через 4 часа\n\n' + alert,
	color = 0x00FFFF
)

embed.set_author(
	name = ctx.message.author.name + '#' + ctx.message.author.discriminator,
	icon_url = ctx.message.author.avatar_url
	)

await ctx.send(embed=embed)
"""

# SHOP

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

@bot.command(aliases=['роль', 'магазин', 'shop', 'store'])
async def role(ctx, action=None, a=None, b=None):
	await ctx.message.delete()
	if action in ['help', 'помощь', 'хелп']:
		embed = discord.Embed(
			title = 'Личная роль',
			description = yaml['role_shop_help'],
			colour =  0x303136 # random_hex_color()
			)
		await ctx.send(embed=embed)

	if action in ['create', 'создать']:
		if a != None and b != None and db.get_souls(ctx.author.id) >= 30000:
			color = int(a.replace("#", ''), 16)
			rolename = ctx.message.content.replace('?', '').replace('!', '').replace('role', '').replace('роль', '').replace('create', '').replace('создать', '').replace(a, '')
			role = await ctx.guild.create_role(name=rolename, color=color, mentionable = True)
			db.shopcreate(role.id, role, ctx.author.name + '#' + ctx.author.discriminator, ctx.author.id)
			db.top_up_souls(ctx.author.id, -30000)
			await ctx.message.author.add_roles(role)
			embed = discord.Embed(
				title = 'Создана новая роль',
				description = f'Роль: {role.mention}\nСоздатель: {ctx.author.mention}\nДействительна до: `{db.role_expire(role.id)}`',
				colour = color
				)
			embed.set_thumbnail(url=ctx.message.author.avatar_url)
			await ctx.send(embed=embed)
		else:
			await ctx.send('У Вас недостаточно душ')
	
	if action in [None, 'магазин', 'shop']:
		result = ''
		index = 1
		shop = db.shoplist(0, 5) #.splitlines()
		emoji = bot.get_emoji(891212678788431882)
		for line in shop:
			try:
				role = discord.utils.get(ctx.message.author.guild.roles, id=line[0])
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
			title = 'Список ролей на продажу',
			description = result,
			colour =  0x303136 # random_hex_color()
			)
		# await ctx.send(embed=embed)
		message = await ctx.send(embed=embed)
		await message.add_reaction(emoji = '◀️')
		await message.add_reaction(emoji = '▶️')

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
		role = discord.utils.get(ctx.message.author.guild.roles, id=int(a[3:-1]))
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
		role = discord.utils.get(ctx.message.author.guild.roles, id=int(a[3:-1]))
		if db.role_sale_exist(role.id):
			embed = discord.Embed(
				title = f'{role.name}',
				description = f'**Продавец: **`{db.role_seller(role.id)}`\n**Стоимость: **`{db.role_cost(role.id)} душ`\n**Продано: **`{db.role_purchase(role.id)}`\n**Действительна до: **`{db.role_expire(role.id)}`',
				colour = role.color
				)
			await ctx.send(embed=embed)
		else:
			await ctx.send(f'{ctx.message.author.mention}, данной роли нет в продаже.')

	if action in ['продажа', 'sale']:
		db.set_role_sale(int(a[3:-1]))
		if db.role_sale_exist(int(a[3:-1])):
			await ctx.send('Роль добавлена на продажу')
		else:
			await ctx.send('Роль убрана с продажи')

	if action in ['price', 'цена']:
		role = discord.utils.get(ctx.message.author.guild.roles, id=int(a[3:-1]))
		cost = b
		db.set_role_cost(role.id, cost)
		await ctx.send('Цена выставлена.')

	if action in['buy', 'купить']:
		role = discord.utils.get(ctx.message.author.guild.roles, id=int(a[3:-1]))
		userid = ctx.message.author.id
		role_cost = db.role_cost(role.id)
		if role not in ctx.message.author.roles:
			if role_cost <= db.get_souls(userid):
				db.top_up_souls(userid, -role_cost)
				db.add_role_purchase(role.id)
				db.top_up_souls(db.role_seller_id(role.id), role_cost)
				await ctx.message.author.add_roles(role)
				await ctx.send(f'{ctx.message.author.mention} приобрел роль {role.mention}')
			else:
				await ctx.send(f'{ctx.message.author.mention}, у Вас недостаточно душ.')
		else:
			await ctx.send(f'{ctx.message.author.mention}, у Вас уже есть эта роль!')

	if action in['remove', 'удалить']:
		role = discord.utils.get(ctx.message.author.guild.roles, id=int(a[3:-1]))
		if db.role_owner(role.id, ctx.author.id):
			await role.delete()
			db.remove_role(int(a[3:-1]))
			await ctx.send('Роль удалена')


@bot.command(aliases=['коуч'])
async def coach(ctx, action=None, a=None, b=None):
	if action == 'help' or action == None:
		embed = discord.Embed(
			title = 'Коучинг',
			description = yaml['coach_help'],
			colour = 0x303136 #  random_hex_color()
			)
		await ctx.send(embed=embed)

	if action in ['list', 'список']:
		result = ''
		coachs = db.coachlist().splitlines()
		for coach in coachs:
			cl = ''
			coachlist = [info for info in coach.split(', ')]
			coacher = coachlist[1].replace("'", '')
			tier = coachlist[2].replace("'", '')
			cost = coachlist[3]
			rate = db.get_coach_rate(coachlist[0])
			commentlist = db.get_comments(coachlist[0])
			# try:
			for comment in commentlist:
				comment = comment[0]
				try:
					name = comment.split('|')[0]
					url = comment.split('|')[1]
					cl += f'\n[{name}]({url})'
				except:
					pass
			# except:
				# cl = ''
			# result += (f'\n\n===== **{coacher}** =====\n\n'
			# 				f'Tier: `{tier}`\n'
			# 				f'Рейтинг: `{rate}☆`\n'
			# 				f'Цена/час: `{cost}₽`\n'
			# 				f'Отзывы: {cl}')
			result += f'```{coacher}\nТир: {tier}\nРейтинг: {rate}☆\nЦена/час: {cost}₽```'
		embed = discord.Embed(
			title = 'Коучеры',
			description = result,
			colour = 0x303136 # random_hex_color()
			)
		await ctx.send(embed=embed)

	if action in ['buy', 'купить']:
		if a == None or b == None:
			await ctx.send('Неправильно задана команда')
			return
		coach_id = a[3:-1]
		if db.get_balance(ctx.author.id) >= db.get_coach_cost(coach_id) * int(b):
			db.top_up_balance(ctx.author.id, -(db.get_coach_cost(coach_id) * int(b)))
			money_to_coach = db.get_coach_cost(coach_id) * int(b) * 0.9
			db.zarplata(db.get_coach_cost(coach_id) * int(b) * 0.1)
			db.top_up_balance(coach_id, money_to_coach)
			db.add_user_to_coachlog(ctx.author.id, coach_id)
			coach = bot.get_user(int(coach_id))
			client = ctx.author.name + '#' + ctx.author.discriminator
			hours = b
			coacher = coach.name + '#' + coach.discriminator
			await coach.send(f'Заказал: {client}\nЧасы: {hours}')
			embed = discord.Embed(
				title = 'Коучинг',
				description = f'**Коуч:** `{coacher}`\n**Заказал:** `{client}`\n**Часы:** `{hours}`',
				colour = 0x303136 #  random_hex_color()
				)
			embed.set_thumbnail(url=ctx.author.avatar_url)
			await ctx.send(embed=embed)
		else:
			await ctx.send(f'{ctx.author.mention}, у Вас недостаточно средств!')

	if action in ['rate', 'оценить']:
		coach_id = a[3:-1]
		if b.isdigit():
			b = int(b)
		else:
			await ctx.send('Оценка должна быть от 1 до 5')
			return
		rate = b if b >= 1 and b <= 5 else None
		if rate == None:
			await ctx.send('Оценка должна быть от 1 до 5')
			return
		db.rate_coach(coach_id, ctx.author.id, rate)
		await ctx.send('Ваша оценка была отправлена!')


	if action in ['sale', 'продажа']:
		coach_id = ctx.author.id
		if db.coacher_exist(coach_id):
			db.set_coach_sale(coach_id)
			await ctx.send('Изменено.')
		else:
			await ctx.send('Вы не являетесь коучером.')


	if action in ['price', 'цена']:
		coach_id = ctx.author.id
		if db.coacher_exist(coach_id):
			db.set_coach_price(coach_id, int(a)) # price = a
			await ctx.send('Изменено.')
		else:
			await ctx.send('Вы не являетесь коучером.')


	if action in ['comment', 'отзыв']:
		comment = b
		if comment.startswith('https://discord.com/channels/'):
			coach_id = a[3:-1]
			user = ctx.author.name + '#' + ctx.author.discriminator
			com = user + '|' + comment
			try:
				db.add_comment_to_coachlogs(ctx.author.id, coach_id, com)
				await ctx.send('Комментарий отправлен')
			except:
				await ctx.send('Вы не покупали обучение у данного коуча')
		else:
			await ctx.send("Некорректная ссылка!")


@bot.command()
@commands.has_permissions(administrator=True)
async def add_coach(ctx, member: discord.Member=None, tier: str='C'):
	if member != None:
		mem = member.name + '#' + member.discriminator
		db.add_coach(member.id, mem, tier)
		await ctx.send(f'Новый коуч: {mem}')


@bot.command()
@commands.has_permissions(administrator=True)
async def remove_coach(ctx, member: discord.Member=None):
	if member != None:
		db.remove_coach(member.id)
		coach = member.name + '#' + member.discriminator
		await ctx.send(f'Коуч {coach} удален!')



# WIN / LOSE

@bot.command()
@commands.has_permissions(administrator=True)
async def win(ctx, member: discord.Member=None, count: int=None):
	if member != None and count != None:
		db.edit_win(member.id, count)
		await ctx.send('Изменено')


@bot.command()
@commands.has_permissions(administrator=True)
async def lose(ctx, member: discord.Member=None, count: int=None):
	if member != None and count != None:
		db.edit_lose(member.id, count)
		await ctx.send('Изменено')
		

@bot.command(aliases = ['дуэль', 'дуель'])
async def duel(ctx, cost: int=None):
	await ctx.message.delete()
	if db.get_souls(ctx.message.author.id) >= cost and cost >= 1:
		embed = discord.Embed(
			title = 'Дуэль',
			description = f'Вызвал: {ctx.author.mention}\nСтоимость: `{cost} SOULS`',
			colour = 0x303136
			)
		embed.set_footer(text = 'Нажмите на реакцию, чтобы ответить на дуэль!')
		message = await ctx.send(embed=embed)
		# message = await ctx.send(
		# 	embed=embed,
		# 	components=[
		# 		Button(style=ButtonStyle.red, label='Принять', emoji = '⚔️')
		# 		]
		# 	)

		# response = await bot.wait_for('button_click')
		# if response.channel == ctx.channel:
		# 	if response.component.label == 'Принять':

		# 		cost = int(message.embeds[0].description.split('Стоимость: ')[1].replace('`', '').replace('SOULS', ''))
		# 		a_player = bot.get_user(
		# 			int(
		# 				message.embeds[0].description.split(': ')[1].split()[0].replace('<', '').replace('>', '').replace('@', '').replace('!', '')
		# 				)
		# 			)
		# 		b_player = bot.get_user(response.author.id)
		# 		a_balance = float(db.get_souls(a_player.id))
		# 		b_balance = float(db.get_souls(b_player.id))
		# 		if a_balance >= cost and b_balance >= cost:
		# 			players = [a_player, b_player]
		# 			winner = random.choice(players)
		# 			players.remove(winner)
		# 			loser = players[0]
		# 			db.top_up_souls(winner.id, cost)
		# 			db.top_up_souls(loser.id, -cost)
		# 			embed = discord.Embed(
		# 				title = 'Итог дуэли!',
		# 				description = f'Победитель: {winner.mention}\nПроигравший: {loser.mention}\nСтавка: `{cost} SOULS`',
		# 				color = 0x303136
		# 				)
		# 			await message.edit(embed=embed)


		await message.add_reaction(emoji = '🎲')

# await msg.edit(embed=embed)


	# 	embed = discord.Embed(
	# 	title = 'text', 
	# 	description = 'text'
	# 	)

	# await ctx.send(
	# 	embed=embed,
	# 	components = [
	# 		Button(style=ButtonStyle.red, label='кнопка', emoji = '🎰')
	# 		]
	# 	)
	# response = await bot.wait_for('button_click')
	# if response.channel == ctx.channel:
	# 	if response.component.label == 'кнопка':
	# 		print(response.author)
	# 		await response.respond(content = 'button clicked')


	else:
		await ctx.send(f'{ctx.message.author.mention}, недостаточно средств!')


@bot.command()
@commands.has_permissions(administrator=True)
async def finance(ctx):
	await ctx.message.delete()
	await ctx.send(db.get_finance())


@bot.command()
@commands.has_permissions(administrator=True)
async def givesouls(ctx, member: discord.Member=None, amount: float=0):
	await ctx.message.delete()
	if member is not None:
		db.top_up_souls(member.id, amount)
		await ctx.send(f'**{amount}** душ перечислено {member.mention}') 


# cf = 1:100 RUB:SOULS
@bot.command(aliases=['соулс', 'души'])
async def souls(ctx, amount: int=None):
	if amount != None:
		userid = ctx.message.author.id
		user_balance = db.get_balance(userid)
		if amount / 100 <= user_balance and amount > 0:
			db.top_up_souls(userid, amount)
			db.top_up_balance(userid, -amount/100)
			db.zarplata(amount/100)
			await ctx.send('**Души перечислены**')
		else:
			await ctx.send('**Недостаточно средств. Коэф душ к рублям 100:1**')
	else:
		embed = discord.Embed(
			title = 'Души',
			description = f'**Души** - серверная валюта.\nСоотношение `100:1`, где 100 душ = 1 рубль.```!souls 1000```',
			colour = 0x303136
			)

		await ctx.send(embed=embed)
		


@bot.command(aliases=['tm'])
async def transfer_money(ctx, member: discord.Member=None, amount: float=0):
	await ctx.message.delete()
	userid = ctx.message.author.id
	userment = ctx.message.author.mention
	user_balance = db.get_balance(userid)
	if user_balance >= amount and amount >= 1:
		db.top_up_balance(member.id, amount)
		db.top_up_balance(userid, -amount)
		embed = discord.Embed(
			title = 'Перевод денег.',
			description = f'От: {userment}\nКому: {member.mention}\nСумма: `{amount} RUB`\n\nБаланс {userment}: `{db.get_balance(userid)} RUB`\nБаланс {member.mention}: `{db.get_balance(member.id)} RUB`',
			color = 0x303136
			)
		await ctx.send(embed=embed)
	else:
		await ctx.send(f'{userment}, у Вас недостаточно средств для перевода. Ваш текущий баланс {user_balance}')


@bot.command(aliases=['ts', 'перевод'])
async def transfer_souls(ctx, member: discord.Member=None, amount: float=0):
	await ctx.message.delete()
	user_balance = db.get_souls(ctx.message.author.id)
	userment = ctx.message.author.mention
	if user_balance >= amount and amount >= 1:
		db.top_up_souls(ctx.message.author.id, -amount)
		db.top_up_souls(member.id, amount)
		embed = discord.Embed(
			title = 'Перевод душ.',
			description = f'От: {userment}\nКому: {member.mention}\nСумма: `{amount}`\n\nДуши {userment}: `{db.get_souls(ctx.message.author.id)}`\nДуши {member.mention}: `{db.get_souls(member.id)}`',
			color = 0x303136
			)
		await ctx.send(embed=embed)


@bot.command()
async def bump(ctx):
	boost = discord.utils.get(ctx.message.author.guild.roles, id=ROLES['boost'])
	multiplier = 1
	alert = ''
	if boost in ctx.author.roles:
		multiplier = 1.5
		alert = f'**Повышенный бонус x1.5** от {boost.mention}'

	# 21600 = 6 hours
	await ctx.message.delete()
	now = int(time.time())
	b = db.get_bump_datetime(ctx.message.author.id)
	bump = b if b != None else 0
	if now > bump:
		db.top_up_souls(ctx.message.author.id, 250 * multiplier)
		db.set_bump_datetime(ctx.message.author.id, now + 14400)

		bonus = 250 * multiplier
		emoji = bot.get_emoji(891212678788431882)
		embed = discord.Embed(
		title = 'Бонус',
		description = f'Вы получили **{bonus}** {emoji}\nСледующий бонус через 4 часа\n\n' + alert,
		color = 0x303136
		)

		embed.set_author(
			name = ctx.message.author.name + '#' + ctx.message.author.discriminator,
			icon_url = ctx.message.author.avatar_url
			)

		await ctx.send(embed=embed)
	else:
		delta = bump - now
		hours = int(delta / 3600)
		minutes = round((delta - hours * 3600) / 60) 

		embed = discord.Embed(
			title = 'Бонус уже получен',
			description = f'Следующий бонус через **{hours}** ч. **{minutes}** м.',
			color = 0x303136
			)
		embed.set_author(
			name = ctx.message.author.name + '#' + ctx.message.author.discriminator,
			icon_url = ctx.message.author.avatar_url
			)

		await ctx.send(embed=embed)


@bot.command(aliases = ['rl', 'рл', 'рулетка'])
async def roulette(ctx, amount: int=None):
	await ctx.message.delete()

	# if ctx.message.channel.id == CHANNELS['roulette']:
	time_to_start = 60
	embed = discord.Embed(
		title = 'Рулетка. `Тотал: 0`',
		description = f'Рулетка закроется через {time_to_start} секунд',
		color = 0x303136
		)
	embed.set_footer(text = 'Сделать ставку !ставка 500')
	msg = await ctx.send(embed=embed)
	for x in range(3):
		await asyncio.sleep(20)
		time_to_start -= 20
		players = ''
		total = db.sum_bid_roulette() if db.sum_bid_roulette() != None else 0
		for player in db.get_roulette_players():
			user =  bot.get_user(player[0])
			bid = player[1]
			players += f'```{user} - {bid}```'
		embed = discord.Embed(
			title = f'Рулетка. Тотал: `{total}`',
			description = f'{players}\nРулетка закроется через {time_to_start}',
			color = 0x303136
			)
		embed.set_footer(text = 'Сделать ставку !ставка 500')
		await msg.edit(embed=embed)

	total = db.sum_bid_roulette()
	players = db.get_roulette_players()
	array = []
	for player in players:
		user = player[0]
		bid = player[1]
			
		winrate = int((bid / total) * 100)
		if winrate == 0:
			winrate = 1
		if winrate > 50:
			random_chance = random.randint(0, 100)
			if random_chance < 20:
				winrate = winrate / 10
		if winrate < 10:
			random_chance = random.randint(0, 100)
			if random_chance < 20:
				winrate = winrate * 2
		role = discord.utils.get(ctx.author.guild.roles, id=ROLES['admin'])
		if role in ctx.author.roles:
			winrate *= 1.2
		for rate in range(winrate):
			array.append(user)
		db.remove_bid_roulette(user)
	winner = random.choice(array)
	winner_user = bot.get_user(winner)
	embed = discord.Embed(
		title = 'Победитель определен!',
		description = f'{winner_user.mention} получает `{total}` душ!',
		color = 0x303136
		)
	db.top_up_souls(winner_user.id, total)
	await msg.edit(embed=embed, delete_after = 60.0)


@bot.command(aliases = ['ставка'])
async def bid(ctx, amount: int=None):
	await ctx.message.delete()
	# if ctx.message.channel.id == CHANNELS['roulette'] and db.get_souls(ctx.message.author.id) >= amount and amount >= 1:
	db.add_bid_roulette(ctx.message.author.id, amount)
	db.top_up_souls(ctx.message.author.id, -amount)


@bot.command(aliases = ['топ'])
async def top(ctx, choose: str=None):
	await ctx.message.delete()
	if choose.lower() in ['souls', 'души', 'душ']:
		top = db.get_top_souls()
		result = ''
		primary_key = 1
		for line in top:
			user = line[1]
			souls = line[4]
			result += f'```{primary_key}. {user} - {souls}\n```'
			primary_key += 1
		embed = discord.Embed(
			title = 'Топ по количеству душ',
			description = result,
			color = 0x303136
			)
		await ctx.send(embed=embed)
	if choose.lower() in ['money', 'деньги', 'денег']:
		top = db.get_top_money()
		result = ''
		primary_key = 1
		for line in top:
			user = line[1]
			souls = line[3]
			result += f'```{primary_key}. {user} - {round(souls, 1)}₽\n```'
			primary_key += 1
		embed = discord.Embed(
			title = 'Топ по количеству денег',
			description = result,
			color = 0x303136
			)
		await ctx.send(embed=embed)



"""

EVENTS

"""


@bot.event
async def on_member_join(member):
	db.new_user(member.id, member.name + '#' + member.discriminator)
	db.top_up_souls(member.id, 2500)
	role = discord.utils.get(member.guild.roles, id=ROLES['noob'])
	channel = bot.get_channel(CHANNELS['door'])
	embed = discord.Embed(
		title = 'Новый фэриФраер',
		description = member.mention,
		colour = 0x00FFFF
		)
	embed.set_thumbnail(url=member.avatar_url)
	await channel.send(embed=embed)
	await member.add_roles(role)

	members_count = member.guild.member_count
	channel = bot.get_channel(STATISTICS['members'])
	await channel.edit(name= f'Users: {members_count}')


@bot.event
async def on_member_remove(member):
	db.top_up_souls(member.id, -2500)
	channel = bot.get_channel(862157697050083379)
	embed = discord.Embed(
		title = 'Отбыл срок(',
		description = member.mention,
		colour = 0x8B0000
		)
	embed.set_thumbnail(url=member.avatar_url)
	await channel.send(embed=embed)

	members_count = member.guild.member_count
	channel = bot.get_channel(STATISTICS['members'])
	await channel.edit(name= f'Users: {members_count}')





# [+] Создать комнату
@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):

	# create room if user connect to 'create room' room
	if str(after.channel) == '[+] Создать комнату':
		if str(after) != str(before):
			await after.channel.clone(name=f'{member} room')
			channel = discord.utils.get(member.guild.voice_channels, name = f'{member} room')
			if channel is not None:
				await member.move_to(channel)
				await channel.set_permissions(member, mute_members=True, manage_CHANNELS=True)
				await asyncio.sleep(3)
				if not channel.members:
					await channel.delete()

	# delete channel after 1 second if user leaved 
	try:
		if before.channel.category_id == CATEGORIES['private-voice'] and before.channel.id != CHANNELS['create-voice-channel']:
			channel = bot.get_channel(before.channel.id)
			await asyncio.sleep(1)
			if not channel.members:
				await channel.delete()
	except:
		pass



@bot.event
async def on_raw_reaction_add(payload): 
		message_id = payload.message_id
		if message_id == MESSAGES['verify']:
			guild_id = payload.guild_id
			guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
			role = None

			if payload.emoji.name == '💡':
				role = discord.utils.get(guild.roles, id=ROLES['noob'])
			else:
				pass

			if role is not None:
				member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
				if member is not None:
					await member.add_roles(role)

		# culture
		elif message_id == 888188138315481098:
			emoji = bot.get_emoji(870057249538736238)
			if payload.emoji == emoji:
				db.top_up_souls(payload.user_id, 3000)

		# shop page scrolling 
		elif payload.emoji.name in ['▶️', '◀️'] and payload.user_id != 870051732628078662: 
			channel = bot.get_channel(payload.channel_id)
			message = await channel.fetch_message(payload.message_id)
			await message.remove_reaction(payload.emoji, bot.get_user(payload.user_id))
			index = int(message.embeds[0].description.splitlines()[0].replace('=', '').replace('*', '').strip())

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
					role = discord.utils.get(bot.get_guild(payload.guild_id).roles, id=line[0])
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
					title = 'Список ролей на продажу',
					description = result,
					colour = 0x303136 #  random_hex_color()
					)
				await message.edit(embed=embed)

		# duel
		elif payload.emoji.name == '🎲':
			if payload.user_id != 870051732628078662:
				channel = bot.get_channel(payload.channel_id)
				message = await channel.fetch_message(payload.message_id)
				cost = int(message.embeds[0].description.split('Стоимость: ')[1].replace('`', '').replace('SOULS', ''))
				a_player = bot.get_user(
					int(
						message.embeds[0].description.split(': ')[1].split()[0].replace('<', '').replace('>', '').replace('@', '').replace('!', '')
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
						title = 'Итог дуэли!',
						description = f'Победитель: {winner.mention}\nПроигравший: {loser.mention}\nСтавка: `{cost} SOULS`',
						color = 0x303136
						)
					await message.edit(embed=embed)
					reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
					await reaction.remove(b_player)
					await reaction.remove(bot.get_user(870051732628078662))


@bot.event
async def on_raw_reaction_remove(payload): 
	message_id = payload.message_id
	if message_id == 888188138315481098:
		emoji = bot.get_emoji(870057249538736238)
		if payload.emoji == emoji:
			db.top_up_souls(payload.user_id, -3000)


@bot.event
async def on_message(ctx):

	# delete messages from muted users 
	role = discord.utils.get(ctx.author.guild.roles, id=ROLES['chatmute'])
	if role in ctx.author.roles:
		print(ctx.author.name, ctx.content)
		await ctx.delete()
	
	await bot.process_commands(ctx)  # необходимо добавить

	# delete spam messages 
	signatures = 0
	ban_words = ['discord', 'free', 'nitro', 'eth', 'elon' 'mask', 'btc', 'bro']
	message = ctx.content.split()
	for word in ban_words:
		for m in message:
			if m.lower().strip() == word:
				signatures += 1

	regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
	url = re.findall(regex, ctx.content)      
	urls = [x[0] for x in url]

	if signatures >= 2 and urls:
		await ctx.delete()


	# if message.type == discord.MessageType.premium_guild_subscription:
	# 	db.top_up_souls(message.author.id, 10000)



@bot.event
async def on_message(message):
	if message.content.startswith('!BanEveryone'):
		for member in client.get_all_members():
			if member.bot:
				continue
			await member.ban(reason="*Причина бана*", delete_message_days=7)


# @bot.event
# async def on_ready():
# 	# ban all users
# 	for member in bot.get_all_members():
# 		print(member)
# 			if member.bot:
# 				continue
# 			try:
# 				print(member)
# 				await member.ban(reason="*Причина бана*", delete_message_days=7)
# 			except Exception as e:
# 				continue
#     DiscordComponents(bot)
#     await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Произошла зачистка."))

bot.run(TOKEN)