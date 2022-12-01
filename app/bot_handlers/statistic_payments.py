from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from datetime import datetime
import db_config


async def stat(message: types.Message):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	buttons = ["Підсумок", "Детально"]
	keyboard.add(*buttons)

	await message.answer("Оберіть вид інформації:", reply_markup=keyboard)


async def result(message: types.Message, state: FSMContext):
	await state.finish()
	chat_id = message.chat.id

	res = db_config.get_stat_for_curr_month(db_config.create_conn_psc2(), chat_id)
	print(res)
	if not res:
		await message.answer("Ще не має статистики..")
	else:
		answ = ""
		for i in res:
			tmp = i.split(',')
			answ += f"{tmp[0]} — {tmp[1]} грн<br>"
		await message.answer(answ, parse_mode='html')


async def detail(message: types.Message, state: FSMContext):
	await state.finish()
	chat_id = message.chat.id

	res = db_config.get_detail_stat_for_curr_month(db_config.create_conn_psc2(), chat_id)

	msg = ""

	for i in res:
		tmp = i.replace('(', '').replace(')', '').split(',')
		tmp[1] = datetime.fromisoformat(tmp[1].replace('"', '')).strftime('%d-%m-%Y')
		msg += f"✅️ <i>{tmp[1]}</i> <code>[{tmp[0]}]</code> — <b>{tmp[3]} грн</b> 👉 {tmp[2]}\n"

	await message.answer(msg, parse_mode='html')


def register_handlers_stat(dp: Dispatcher):
	dp.register_message_handler(stat, commands="stat", state="*")
	dp.register_message_handler(stat, CommandStart(deep_link="stat"), state="*")
	dp.register_message_handler(result, Text(equals="Підсумок", ignore_case=True), state="*")
	dp.register_message_handler(detail, Text(equals="Детально", ignore_case=True), state="*")


