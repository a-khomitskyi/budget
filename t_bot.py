from telebot import TeleBot, types
from os import getenv
from dotenv import load_dotenv
from logging import Logger
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(name)s] - %(message)s', datefmt='%H:%M:%S')
load_dotenv()
bot = TeleBot(getenv("TOKEN"))


@bot.message_handler(commands=['start'])
def bot_start(message: types.Message):
	bot.send_message(chat_id=message.chat.id,
					 text=f"<b>Привіт, {message.from_user.full_name}</b>!\n\nЯ Бот, що займається підрахунком витрат. Ось основиний перелік того, що я вмію:\n<code>/add</code> — Додати покупку в список;\n<code>/stat</code> — Вивести статистику витрат за поточний місяць;\n<code>/revise</code> — Вивести статистику витрат помісячно за поточний рік;\n<code>/edit</code> — Редагувати додану покупку\n<code>/help</code> — Інформація щодо бота\n\nНумо починати!",
					 parse_mode='html')


@bot.message_handler(commands=['help'])
def bot_start(message: types.Message):
	bot.send_message(chat_id=message.chat.id,
					 text=f"Привіт, {message.from_user.full_name}!\nЯ Бот, що займається підрахунком витрат. Нумо починати!")


@bot.message_handler(commands=['add'])
def bot_start(message: types.Message):
	bot.send_message(chat_id=message.chat.id,
					 text=f"Привіт, {message.from_user.full_name}!\nЯ Бот, що займається підрахунком витрат. Нумо починати!")


@bot.message_handler(commands=['stat'])
def bot_start(message: types.Message):
	bot.send_message(chat_id=message.chat.id,
					 text=f"Привіт, {message.from_user.full_name}!\nЯ Бот, що займається підрахунком витрат. Нумо починати!")


@bot.message_handler(commands=['edit'])
def bot_start(message: types.Message):
	bot.send_message(chat_id=message.chat.id,
					 text=f"Привіт, {message.from_user.full_name}!\nЯ Бот, що займається підрахунком витрат. Нумо починати!")


if __name__ == '__main__':
	bot.infinity_polling()
