import sqlite3


def create_connection(db_file):
	""" create a database connection to the SQLite database
		specified by db_file
	:param db_file: database file
	:return: Connection object or None
	"""
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except sqlite3.Error as e:
		print(e)

	return conn


def save_payment(conn, data):
	"""
	Create a new payment
	:param conn:
	:param data:
	:return:
	"""

	sql = "INSERT INTO chat (chat_id, user_id, title, price) VALUES(?,?,?,?)"
	cur = conn.cursor()
	cur.execute(sql, data)
	conn.commit()

	return cur.lastrowid


# def get_user_state(conn, user_id, chat_id):
# 	try:
# 		sql = f"SELECT state FROM states WHERE user_id={user_id} and chat_id={chat_id}"
# 		cur = conn.cursor()
# 		cur.execute(sql)
# 		result = cur.fetchall()
# 		conn.close()
#
# 	return result
