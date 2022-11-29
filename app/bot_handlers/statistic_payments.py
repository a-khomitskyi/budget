from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters.builtin import CommandStart
from dotenv import load_dotenv
from os import getenv
import db_config

load_dotenv()


class AddStates(StatesGroup):
	add_title = State()
	add_price = State()


async def stat(message: types.Message):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	buttons = ["Підсумок", "Аналіз"]
	keyboard.add(*buttons)

	await message.answer("Оберіть вид інформації:", reply_markup=keyboard)


async def result(message: types.Message):
	chat_id = message.chat.id





def register_handlers_add(dp: Dispatcher):
	dp.register_message_handler(stat, commands="stat", state="*")
	dp.register_message_handler(stat, CommandStart(deep_link="stat"), state="*")
	dp.register_message_handler(result, Text(equals="Підсумок", ignore_case=True), state="*")
	dp.register_message_handler(stat, Text(equals="Аналіз витрат", ignore_case=True), state="*")
	# dp.register_message_handler(title_added, state=AddStates.add_title)

