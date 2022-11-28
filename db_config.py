import logging
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


def get_stat_for_curr_month(conn, chat_id):
	try:
		sql = f"SELECT (user_id, price) FROM chat WHERE chat_id={chat_id} and EXTRACT(MONTH FROM created_at)=EXTRACT(MONTH FROM CURRENT_DATE) and EXTRACT(YEAR FROM created_at)=EXTRACT(YEAR FROM CURRENT_DATE) GROUP BY user_id"
		cur = conn.cursor()
		cur.execute(sql)
		result = cur.fetchall()
		conn.close()
	except Exception as _e:
		print(_e)
	return result


if __name__ == '__main__':
	save_payment(create_connection('db.sqlite'), [123213131, 12312312312, "test", "test"])

