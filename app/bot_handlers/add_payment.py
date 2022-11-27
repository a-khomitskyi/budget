from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters.builtin import CommandStart
import db_config
import os.path


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "db.sqlite")


class AddStates(StatesGroup):
	add_title = State()
	add_price = State()


async def add_payment(message: types.Message):
	await message.answer("Що купили?:")
	await AddStates.add_title.set()


async def title_added(message: types.Message, state: FSMContext):
	await state.update_data(title=message.text.strip())
	await message.answer("Скільки витратили?")
	await AddStates.add_price.set()


async def price_added(message: types.Message, state: FSMContext):
	user_data = await state.get_data()

	# Падає помилка...
	# db_config.save_payment(db_config.create_connection(db_path),
	# 			 [message.from_user.id, message.chat.id, user_data['title'], message.text.strip()])
	await message.answer("Готово!")
	await state.finish()


def register_handlers_add(dp: Dispatcher):
	dp.register_message_handler(add_payment, commands="add", state="*")
	dp.register_message_handler(add_payment, CommandStart(deep_link="add"), state="*")
	dp.register_message_handler(title_added, state=AddStates.add_title)
	dp.register_message_handler(price_added, state=AddStates.add_price)
