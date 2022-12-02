import sqlite3
import psycopg2
from dotenv import load_dotenv
from os import getenv

load_dotenv()


def create_conn_psc2():
	conn = None
	try:
		conn = psycopg2.connect(
			database=getenv("DB_NAME"),
			user=getenv("DB_USER"),
			password=getenv("DB_PASS"),
			host=getenv("DB_HOST"),
			port=getenv("DB_PORT")
		)
	except psycopg2.Error as _e:
		print(_e)

	return conn


def save_payment(conn, data):
	"""
	Create a new payment
	:param conn:
	:param data:
	:return:
	"""

	sql = "INSERT INTO chat (chat_id, user_id, title, price) VALUES(%s, %s, %s, %s)"
	cur = conn.cursor()
	cur.execute(sql, data)
	conn.commit()

	return cur.lastrowid


def get_stat_for_curr_month(conn, chat_id):
	result = None

	try:
		sql = f"SELECT (user_id, SUM(price)) FROM chat WHERE chat_id={chat_id} and EXTRACT(MONTH FROM created_at)=EXTRACT(MONTH FROM CURRENT_DATE) and EXTRACT(YEAR FROM created_at)=EXTRACT(YEAR FROM CURRENT_DATE) GROUP BY user_id"
		cur = conn.cursor()
		cur.execute(sql)
		# result = cur.fetchall()
		result = [x[0].replace('(', '').replace(')', '') for x in cur.fetchall()]
		conn.close()
	except Exception as _e:
		print(_e)
	return result


def get_detail_stat_for_curr_month(conn, chat_id):
	result = None

	try:
		sql = f"SELECT (user_id, created_at, title, price) FROM chat WHERE chat_id={chat_id} and EXTRACT(MONTH FROM created_at)=EXTRACT(MONTH FROM CURRENT_DATE) and EXTRACT(YEAR FROM created_at)=EXTRACT(YEAR FROM CURRENT_DATE)"
		cur = conn.cursor()
		cur.execute(sql)
		result = [item[0] for item in cur.fetchall()]
		conn.close()
	except Exception as _e:
		print(_e)
	return result


def get_stat_for_any_month(conn, chat_id, date):
	result = None

	try:
		sql = f"SELECT (user_id, SUM(price)) FROM chat WHERE chat_id={chat_id} and EXTRACT(MONTH FROM created_at)={date[0]} and EXTRACT(YEAR FROM created_at)={date[-1]} GROUP BY user_id"
		cur = conn.cursor()
		cur.execute(sql)
		result = [x[0].replace('(', '').replace(')', '') for x in cur.fetchall()]
		conn.close()
	except Exception as _e:
		print(_e)
	return result


def get_detail_stat_for_any_month(conn, chat_id, date):
	result = None

	try:
		sql = f"SELECT (user_id, created_at, title, price) FROM chat WHERE chat_id={chat_id} and EXTRACT(MONTH FROM created_at)={date[0]} and EXTRACT(YEAR FROM created_at)={date[-1]}"
		cur = conn.cursor()
		cur.execute(sql)
		result = cur.fetchall()
		conn.close()
	except Exception as _e:
		print(_e)
	return result


def get_month(conn, chat_id):
	# [int(x[0]) for x in t]
	result = None

	try:
		sql = f"SELECT DISTINCT EXTRACT(MONTH FROM created_at) FROM chat WHERE chat_id={chat_id} and EXTRACT(YEAR FROM created_at)=EXTRACT(YEAR FROM CURRENT_DATE)"
		cur = conn.cursor()
		cur.execute(sql)
		result = [int(x[0]) for x in cur.fetchall()]
		conn.close()
	except Exception as _e:
		print(_e)
	return result


def revise_all_year(conn, chat_id, month):
	result = None

	try:
		sql = f"SELECT (user_id, SUM(price)) FROM chat WHERE chat_id={chat_id} and EXTRACT(MONTH FROM created_at)={month} and EXTRACT(YEAR FROM created_at)=EXTRACT(YEAR FROM CURRENT_DATE) GROUP BY user_id"
		cur = conn.cursor()
		cur.execute(sql)
		result = cur.fetchall()
		conn.close()
	except Exception as _e:
		print(_e)
	return result


def get_last_records(conn, chat_id, user_id):
	result = None

	try:
		sql = f"SELECT (pid, user_id, created_at, title, price) FROM chat WHERE chat_id={chat_id} and user_id={user_id} and EXTRACT(MONTH FROM created_at)=EXTRACT(MONTH FROM CURRENT_DATE) and EXTRACT(YEAR FROM created_at)=EXTRACT(YEAR FROM CURRENT_DATE)"
		cur = conn.cursor()
		cur.execute(sql)
		result = cur.fetchall()
		conn.close()
	except Exception as _e:
		print(_e)
	return result


def update_payment(conn, data):
	sql = "INSERT INTO chat (chat_id, user_id, title, price) VALUES(%s, %s, %s, %s)"
	cur = conn.cursor()
	cur.execute(sql, data)
	conn.commit()

	return cur.lastrowid


def delete_payment(conn, row_id):
	sql = f"DELETE FROM chat WHERE pid=%s"
	cur = conn.cursor()
	cur.execute(sql, row_id)
	conn.commit()

	return cur.lastrowid


if __name__ == '__main__':
	# save_payment(create_connection('db.sqlite'), [123213131, 12312312312, "test", "test"])
	# save_payment(create_conn_psc2(), [123213131, 12312312312, "test", 123.12])
	# print(get_stat_for_curr_month(create_conn_psc2(), 305819779))
	# print(get_detail_stat_for_curr_month(create_conn_psc2(), 305819779))
	print(revise_for_year(create_conn_psc2(), 305819779))
