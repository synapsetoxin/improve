# coding: utf-8

import sqlite3
import datetime as dt


class Database():
	def database_connect(func):
		def connect(*args):
			with sqlite3.connect('database.db') as conn:
				cursor = conn.cursor()
				function = func(*args, cursor)
				conn.commit()
				return function
		return connect


	@database_connect
	def launched(cur):
		try:
			cur.execute('SELECT * FROM users')
			cur.execute('SELECT * FROM passwords')
			return '[+] database launched'
		except:
			return '[!] database is not launched'


	@database_connect
	def new_user(userid, username, cur):
		try:
			cur.execute(
				"INSERT INTO users(userid, username) VALUES (?, ?);", 
				[userid, username]
				)
		except:
			cur.execute(
				"UPDATE users SET username = ? WHERE userid = ?", 
				[username, userid]
				)


	@database_connect
	def select_all(cur):
		try:
			cur.execute("SELECT * FROM users")
			result = cur.fetchall()
			replaces = {
				"),": "\n",
				")": "",
				"(": "",
				"[": "",
				"]": ""}
			for i, j in replaces.items(): result = str(result).replace(i, j)
			return result
		except Exception as e:
			print(e)


	@database_connect
	def get_userid_from_dotaid(dota_id, cur):
		return cur.execute(
			'SELECT userid FROM users WHERE dotaid = ?', [dota_id]
			).fetchone()[0]


	@database_connect
	def get_userid(userid, cur):
		return cur.execute(
			"SELECT userid FROM users WHERE userid = ?", 
			[userid]).fetchone()[0]


	@database_connect
	def get_username(userid, cur):
		return cur.execute(
			"SELECT username FROM users WHERE userid = ?", 
			[userid]).fetchone()[0]


	@database_connect
	def get_dotaid(userid, cur):
		return cur.execute(
			"SELECT dotaid FROM users WHERE userid = ?", 
			[userid]).fetchone()[0]


	@database_connect
	def get_balance(userid, cur):
		return cur.execute(
			"SELECT balance FROM users WHERE userid = ?", 
			[userid]).fetchone()[0]


	@database_connect
	def get_souls(userid, cur):
		return cur.execute(
			"SELECT souls FROM users WHERE userid = ?", 
			[userid]).fetchone()[0]


	@database_connect
	def get_wins(userid, cur):
		return cur.execute(
			"SELECT win FROM users WHERE userid = ?", 
			[userid]).fetchone()[0]


	@database_connect
	def get_loses(userid, cur):
		return cur.execute(
			"SELECT lose FROM users WHERE userid = ?", 
			[userid]).fetchone()[0]


	@database_connect
	def set_dotaid(userid, dotaid, cur):
		try:
			cur.execute(
				"INSERT INTO users(userid, dotaid) VALUES (?, ?);", 
				[userid, dotaid]
				)
		except:
			cur.execute(
				"UPDATE users SET dotaid = ? WHERE userid = ?", 
				[dotaid, userid]
				)


	@database_connect
	def tournament_registration(userid, dotaid, cur):
		cur.execute(
			'INSERT INTO freetournament(userid, dotaid) VALUES (?, ?)',
			[userid, dotaid]
			)
		# if cost == None:
		#     dotaid = cur.execute(
		#         'SELECT dotaid FROM users WHERE userid = ?'
		#         ).fetchone()[0]
		#     cur.execute(
		#         'INSERT INTO freetournament(userid, dotaid) VALUES (?, ?)',
		#         [userid, dotaid]
		#         )
		# else:
		#     balance = = cur.execute(
		#         'SELECT balance FROM users WHERE userid = ?'
		#         ).fetchone()[0]
		#     if balance >= cost:
		#         pass
		#     else:
		#         raise 


	@database_connect
	def tournament_unregistration(userid, cur):
		cur.execute(
			'DELETE FROM freetournament WHERE userid = ?', [userid]
			)
		# if cost == None:
		#     dotaid = cur.execute(
		#         'SELECT dotaid FROM users WHERE userid = ?'
		#         ).fetchone()[0]
		#     cur.execute(
		#         'INSERT INTO freetournament(userid, dotaid) VALUES (?, ?)',
		#         [userid, dotaid]
		#         )
		# else:
		#     balance = = cur.execute(
		#         'SELECT balance FROM users WHERE userid = ?'
		#         ).fetchone()[0]
		#     if balance >= cost:
		#         pass
		#     else:
		#         raise 


	@database_connect
	def create_tournament(cur):
		cur.execute(f"""CREATE TABLE freetournament (
userid     INT  UNIQUE,
dotaid     INT  UNIQUE
);""")


	@database_connect
	def remove_tournament(cur):
		cur.execute('DROP TABLE freetournament')


	@database_connect
	def reglist(cur):
		cur.execute("SELECT * FROM freetournament")
		result = cur.fetchall()
		replaces = {
			"),": "\n",
			")": "",
			"(": "",
			"[": "",
			"]": ""}
		for i, j in replaces.items(): result = str(result).replace(i, j)
		return result



	@database_connect
	def get_coach_rate(coach_id, cur):
		rates = cur.execute('SELECT SUM(rate) FROM coach_logs WHERE coachid IN (?)', [coach_id]).fetchone()[0]
		rates_count = cur.execute('SELECT COUNT(rate) as count FROM coach_logs').fetchone()[0]
		try:
			rate = rates / rates_count
			return rate
		except:
			return 0


	@database_connect
	def count_tournament_players(cur):
		try:
			count = cur.execute("SELECT COUNT(*) as count FROM freetournament").fetchone()[0]
			if count == None: count = '0'
			return str(count)
		except:
			return '0'


	@database_connect
	def count_lobby_games(userid, cur):
		try:
			count = cur.execute("SELECT COUNT(*) as count FROM lobby WHERE first_player_id = ? AND second_player_id = ?", [userid, userid]).fetchone()[0]
			if count == None: count = '0'
			return str(count)
		except:
			return '0'


	@database_connect
	def toggle_lobby_search(userid, cur):
		current_state = cur.execute('SELECT lobby_status FROM users WHERE userid = ?', [userid]).fetchone()[0]
		if current_state == 0:
			cur.execute('UPDATE users SET lobby_status = 1 WHERE userid = ?', [userid])
		if current_state == 1:
			cur.execute('UPDATE users SET lobby_status = 0 WHERE userid = ?', [userid])


	@database_connect
	def get_lobby_status(userid, cur):
		return cur.execute('SELECT lobby_status FROM users WHERE userid = ?', [userid]).fetchone()[0]


	@database_connect
	def get_users_search_lobby(cur):
		try:
			count = cur.execute("SELECT COUNT(*) as count FROM users WHERE lobby_status = 1").fetchone()[0]
			if count == None: count = '0'
			return str(count)
		except:
			return '0'


	@database_connect
	def get_lobby_players(cur):
		return cur.execute('SELECT userid FROM users WHERE lobby_status = 1').fetchall()


	@database_connect
	def get_lobby_time_between_players(a, b, cur):
		try:
			last_time = cur.execute('SELECT datetime FROM lobby WHERE first_player_id = ? AND second_player_id = ?', [a, b]).fetchone()[0]
			if last_time != None:
				return last_time
			else:
				return 0	
		except:
			return 0


	@database_connect
	def shopcreate(roleid, role, seller, sellerid, cur):
		expire = (dt.datetime.now() + dt.timedelta(days=30)).strftime("%d-%m-%Y")
		cur.execute(
			'INSERT INTO shop(roleid, role, seller, sellerid, expiration) VALUES (?, ?, ?, ?, ?)',
			[roleid, str(role), seller, sellerid, expire]
			)


	@database_connect
	def role_expire(role_id, cur):
		return cur.execute('SELECT expiration FROM shop WHERE roleid = ?', [role_id]).fetchone()[0]


	@database_connect
	def role_seller(role_id, cur):
		return cur.execute('SELECT seller FROM shop WHERE roleid = ?', [role_id]).fetchone()[0]


	@database_connect
	def role_seller_id(role_id, cur):
		return cur.execute('SELECT sellerid FROM shop WHERE roleid = ?', [role_id]).fetchone()[0]


	@database_connect
	def role_purchase(role_id, cur):
		return cur.execute('SELECT purchase FROM shop WHERE roleid = ?', [role_id]).fetchone()[0]


	@database_connect
	def role_cost(role_id, cur):
		return cur.execute('SELECT cost FROM shop WHERE roleid = ?', [role_id]).fetchone()[0]


	@database_connect
	def set_role_sale(role_id, cur):
		sale = cur.execute('SELECT sale FROM shop WHERE roleid = ?', [role_id]).fetchone()[0]
		if sale == 1:
			cur.execute('UPDATE shop SET sale = 0 WHERE roleid = ?', [role_id])
		if sale == 0:
			cur.execute('UPDATE shop SET sale = 1 WHERE roleid = ?', [role_id])


	@database_connect
	def set_role_cost(role_id, cost, cur):
		cur.execute('UPDATE shop SET cost = ? WHERE roleid = ?', [cost, role_id])


	@database_connect
	def get_roles_id(cur):
		return cur.execute('SELECT roleid FROM shop').fetchall()


	@database_connect
	def role_extend(role_id, date, cur):
		cur.execute('UPDATE shop SET expiration = ? WHERE roleid = ?', [date, role_id])


	@database_connect
	def add_role_purchase(role_id, cur):
		current_purchase = cur.execute(
			"SELECT purchase FROM shop WHERE roleid = ?", [role_id]
			).fetchone()[0]
		cur.execute(
			"UPDATE shop SET purchase = ? WHERE roleid = ?",
			[current_purchase + 1, role_id]
			)


	@database_connect
	def shoplist(a, b, cur):
		return cur.execute("SELECT * FROM shop WHERE sale = 1 ORDER BY purchase DESC LIMIT ?, ?", [a, b]).fetchall()


	@database_connect
	def remove_role(role_id, cur):
		cur.execute('DELETE FROM shop WHERE roleid = ?', [role_id])


	@database_connect
	def role_sale_exist(role_id, cur):
		result = cur.execute('SELECT sale FROM shop WHERE roleid = ?', [role_id]).fetchone()[0]
		if result == 1:
			return True
		if result == 0:
			return False


	@database_connect
	def role_owner(role_id, owner_id, cur):
		roles = cur.execute('SELECT roleid FROM shop WHERE sellerid = ?', [owner_id]).fetchall()
		for role in roles:
			if role[0] == role_id:
				return True
		else:
			return False


	@database_connect
	def get_settings(name, cur):
		return cur.execute('SELECT value FROM settings WHERE name = ?', [name]).fetchone()[0]



	@database_connect
	def add_transaction(transaction_id, amount, currency, comment, cur):
		cur.execute(
			'INSERT INTO transactions(transaction_id, amount, currency, comment) VALUES (?, ?, ?, ?)', 
			[transaction_id, amount, currency, comment]
			)


	@database_connect
	def top_up_balance(userid, amount, cur):
		current_balance = cur.execute(
			"SELECT balance FROM users WHERE userid = ?", [userid]
			).fetchone()[0]
		cur.execute(
			"UPDATE users SET balance = ? WHERE userid = ?",
			[current_balance + amount, userid]
			)


	@database_connect
	def check_transaction(transaction_id, cur):
		try:
			result = cur.execute('SELECT currency FROM transactions WHERE transaction_id = ?', 
				[transaction_id]).fetchone()[0]
			return False
		except:
			return True


	@database_connect
	def get_comission(userid, cur):
		pass


	@database_connect
	def top_up_souls(userid, amount, cur):
		current_balance = cur.execute(
			"SELECT souls FROM users WHERE userid = ?", [userid]
			).fetchone()[0]
		cur.execute(
			"UPDATE users SET souls = ? WHERE userid = ?",
			[current_balance + amount, userid]
			)


	@database_connect
	def set_tour_cost(cost, cur):
		cur.execute('UPDATE settings SET value = ? WHERE name = ?', [cost, 'tour_cost'])


	@database_connect
	def get_tour_cost(cur):
		return cur.execute('SELECT value FROM settings WHERE name = ?', ['tour_cost']).fetchone()[0] 


	@database_connect
	def coachlist(cur):
		cur.execute("SELECT * FROM coach")
		result = cur.fetchall()
		replaces = {
			"),": "\n",
			")": "",
			"(": "",
			"[": "",
			"]": ""}
		for i, j in replaces.items(): result = str(result).replace(i, j)
		return result


	@database_connect
	def get_coach_cost(coachid, cur):
		return cur.execute('SELECT cost FROM coach WHERE coachid = ?', [coachid]).fetchone()[0]


	@database_connect
	def zarplata(amount, cur):
		users_count = cur.execute("SELECT COUNT(*) as count FROM finance").fetchone()[0]
		dolya = amount / users_count
		users = cur.execute('SELECT userid FROM finance').fetchall()
		for user in users:
			user = user[0]
			current_balance = cur.execute(
				"SELECT balance FROM finance WHERE userid = ?", [user]
				).fetchone()[0]
			cur.execute(
				"UPDATE finance SET balance = ? WHERE userid = ?",
				[current_balance + dolya, user]
				)


	@database_connect
	def rate_coach(coach_id, user_id, rate, cur):
		user_buyed = cur.execute('SELECT coachid FROM coach_logs WHERE userid = ?', [user_id])
		if user_buyed is not None:
			cur.execute(
				'UPDATE coach_logs SET rate = ? WHERE userid = ? AND coachid = ?', 
				[rate, user_id, coach_id]
				)
		

	@database_connect
	def get_coach_rate(coach_id, cur):
		rates = cur.execute('SELECT SUM(rate) FROM coach_logs WHERE coachid IN (?)', [coach_id]).fetchone()[0]
		rates_count = cur.execute('SELECT COUNT(rate) as count FROM coach_logs').fetchone()[0]
		try:
			rate = rates / rates_count
			return rate
		except:
			return 0


	@database_connect
	def get_coach_tier(coach_id, cur):
		return cur.execute('SELECT tier FROM coach WHERE coachid = ?', [coach_id]).fetchone()[0]


	@database_connect
	def add_user_to_coachlog(user_id, coach_id, cur):
		try:
			cur.execute(
				"INSERT INTO coach_logs(userid, coachid) VALUES (?, ?);", 
				[user_id, coach_id]
				)
		except:
			pass


	@database_connect
	def add_comment_to_coachlogs(userid, coachid, url, cur):
		user_buyed = cur.execute('SELECT coachid FROM coach_logs WHERE userid = ?', [user_id])
		if user_buyed is not None:
			cur.execute(
				'UPDATE coach_logs SET comment = ? WHERE userid = ? AND coachid = ?', 
				[url, userid, coachid]
				)

	@database_connect
	def get_comments(coachid, cur):
		return cur.execute('SELECT comment FROM coach_logs WHERE coachid = ?', [coachid]).fetchall()

	@database_connect
	def set_coach_sale(coach_id, cur):
		sale = cur.execute('SELECT sale FROM coach WHERE coachid = ?', [coach_id]).fetchone()[0]
		if sale == 1:
			cur.execute('UPDATE coach SET sale = 0 WHERE coachid = ?', [coach_id])
		if sale == 0:
			cur.execute('UPDATE coach SET sale = 1 WHERE coachid = ?', [coach_id])


	@database_connect
	def set_coach_price(coach_id, price, cur):
		cur.execute('UPDATE coach SET cost = ? WHERE coachid = ?', [price, coach_id])


	@database_connect
	def coacher_exist(coacher_id, cur):
		try:
			coach = cur.execute('SELECT * FROM coach WHERE coachid = ?', [coacher_id]).fetchone()[0]
			return True 
		except:
			return False


	@database_connect
	def add_coach(user_id, username, tier, cur):
		try:
			cur.execute(
				"INSERT INTO coach(coachid, coachname, tier) VALUES (?, ?, ?);", 
				[user_id, username, tier]
				)
		except:
			cur.execute(
				"UPDATE coach SET coachname = ? WHERE userid = ?", 
				[user_id, username]
				)
			cur.execute(
				"UPDATE coach SET tier = ? WHERE userid = ?", 
				[user_id, tier]
				)


	@database_connect
	def remove_coach(user_id, cur):
		cur.execute('DELETE FROM coach WHERE coachid = ?', [user_id])


	@database_connect
	def edit_win(userid, count, cur):
		current_win = cur.execute(
			"SELECT win FROM users WHERE userid = ?", [userid]
			).fetchone()[0]
		cur.execute(
			"UPDATE users SET win = ? WHERE userid = ?",
			[current_win + count, userid]
			)


	@database_connect
	def edit_lose(userid, count, cur):
		current_lose = cur.execute(
			"SELECT lose FROM users WHERE userid = ?", [userid]
			).fetchone()[0]
		cur.execute(
			"UPDATE users SET lose = ? WHERE userid = ?",
			[current_lose + count, userid]
			)


	@database_connect
	def get_tier_and_pts(user_id, cur):
		tier = 4
		pts = cur.execute('SELECT pts FROM users WHERE userid = ?', [user_id]).fetchone()[0]
		if pts > 3000:
			tier = 3
		if pts > 6000:
			tier = 2
		if pts > 9000:
			tier = 1

		return tier, pts


	@database_connect
	def get_finance(cur):
		finance = cur.execute('SELECT username, balance FROM finance').fetchall()
		result = ''
		for info in finance:
			user = info[0]
			balance = info[1]
			result += f'**{user}:** `{str(round(balance, 2))} RUB`\n'
		return result


	@database_connect
	def user_tournament_registered(user_id, cur):
		result = cur.execute('SELECT userid FROM freetournament WHERE userid = ?', [user_id]).fetchone()[0]
		if result != None:
			return True
		else:
			return False


	@database_connect
	def get_bump_datetime(user_id, cur):
		return cur.execute('SELECT bump FROM users WHERE userid = ?', [user_id]).fetchone()[0]


	@database_connect
	def set_bump_datetime(user_id, time, cur):
		cur.execute('UPDATE users SET bump = ? WHERE userid = ?', [time, user_id])


	@database_connect
	def get_top_souls(cur):
		return cur.execute("SELECT * FROM users ORDER BY souls DESC LIMIT 0, 10").fetchall()


	@database_connect
	def get_top_money(cur):
		return cur.execute("SELECT * FROM users ORDER BY balance DESC LIMIT 0, 10").fetchall()


	@database_connect
	def get_roulette_players(cur):
		return cur.execute('SELECT * FROM roulette ORDER BY bid DESC').fetchall()


	@database_connect
	def add_bid_roulette(user_id, amount, cur):
		try:
			cur.execute('INSERT INTO roulette(userid, bid) VALUES (?, ?)', [user_id, amount])
		except:
			try:
				current_bid = cur.execute(
					"SELECT bid FROM roulette WHERE userid = ?", [user_id]
					).fetchone()[0]
			except:
				current_bid = 0
			cur.execute('UPDATE roulette SET bid = ? WHERE userid = ?',
				[current_bid + amount, user_id]
				)


	@database_connect
	def sum_bid_roulette(cur):
		return cur.execute('SELECT SUM(bid) FROM roulette').fetchone()[0]


	@database_connect
	def remove_bid_roulette(userid, cur):
		cur.execute(
			'DELETE FROM roulette WHERE userid = ?', [userid]
			)


	@database_connect
	def guarantee_exist(userid, cur):
		try:
			user = cur.execute('SELECT * FROM guarantee WHERE userid = ?', [userid]).fetchone()[0]
			return True 
		except:
			return False


	@database_connect
	def check_bank(userid, bank, cur):
		return cur.execute('SELECT ? FROM guarantee WHERE userid = ?', [bank, userid]).fetchone()[0]


	@database_connect
	def bank_list(userid, cur):
		bank = ''
		banks_name_by_id = {
			0: 'Баланс',
			1: 'Души',
			2: 'Steam',
			3: 'Сбербанк',
			4: 'Tinkoff',
			5: 'QIWI',
			6: 'Альфа банк'
		}
		banks_info = cur.execute('SELECT server_balance, souls, steam, sberbank, tinkoff, qiwi, alpha FROM guarantee WHERE userid = ?', [userid]).fetchall()[0]
		for b in enumerate(banks_info):
			if b[1] == 1:
				bank += banks_name_by_id[b[0]] + '\n'
		return bank


	@database_connect
	def get_guarantee_deals(userid, cur):
		pass


	@database_connect
	def get_guarantee_percent(userid, cur):
		return cur.execute('SELECT percent FROM guarantee WHERE userid = ?', [userid]).fetchone()[0]


	@database_connect
	def get_guarantees(cur):
		pass
