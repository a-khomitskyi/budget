from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from datetime import datetime
import db_config
import re


class ReviseStates(StatesGroup):
	add_date = State()
	inactive = State()


async def revise(message: types.Message):
	await message.answer(
		"Вкажіть місяць за який потрібно вивести інформацію:\n<i>Формат </i><code>місяць.рік</code> <i>(05.2022)</i>", parse_mode='html')
	await ReviseStates.add_date.set()


async def entered_date(message: types.Message, state: FSMContext):
	pattern = re.compile(r"0[1-9]|1[0-2]\.202[2-9]")
	if not re.match(pattern, message.text):
		await message.reply("Невірний формат дати. Ось підказка 👉 <code>місяць.рік</code> <i>(05.2022)</i>")
		return

	await state.update_data(date=message.text.split('.'))

	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	buttons = ["Архів", "Увесь час"]
	keyboard.add(*buttons)
	await ReviseStates.inactive.set()
	await message.answer("Оберіть вид інформації:", reply_markup=keyboard)


async def archive(message: types.Message, state: FSMContext):
	chat_id = message.chat.id
	user_date = await state.get_data()
	await state.finish()
	sm = db_config.get_stat_for_any_month(db_config.create_conn_psc2(), chat_id, user_date['date'])
	row_data = db_config.get_detail_stat_for_any_month(db_config.create_conn_psc2(), chat_id, user_date['date'])

	if not row_data:
		await message.answer("За вказаний місяць не існує статистики..")
	else:
		await message.answer("Статистика за month year")
		msg = ""

		for i in row_data:
			tmp = i[0].replace('(', '').replace(')', '').split(',')
			tmp[1] = datetime.fromisoformat(tmp[1].replace('"', '')).strftime('%d-%m-%Y')
			msg += f"✅️ <i>{tmp[1]}</i> <code>[{tmp[0]}]</code> — <b>{tmp[3]} грн</b> 👉 {tmp[2]}\n"

		await message.answer(msg, parse_mode='html')
		answ = ""
		# for i in row_data:
		# 	tmp = i[0].split(',')
		# 	answ += f"<code>[{tmp[0]}]</code> — <b>{tmp[1]}</b> грн\n"
		# await message.answer(answ, parse_mode='html')
		# await message.answer('-----------------------------')
		# answ = ""
		# for i in sm:
		# 	tmp = i.split(',')
		# 	answ += f"<code>[{tmp[0]}]</code> — <b>{tmp[1]}</b> грн\n"
		# await message.answer(answ, parse_mode='html')


async def all_period(message: types.Message, state: FSMContext):
	await state.finish()
	chat_id = message.chat.id

	res = db_config.get_detail_stat_for_curr_month(db_config.create_conn_psc2(), chat_id)

	msg = ""

	for i in res:
		tmp = i.replace('(', '').replace(')', '').split(',')
		tmp[1] = datetime.fromisoformat(tmp[1].replace('"', '')).strftime('%d-%m-%Y')
		msg += f"✅️ <i>{tmp[1]}</i> <code>[{tmp[0]}]</code> — <b>{tmp[3]} грн</b> 👉 {tmp[2]}\n"

	await message.answer(msg, parse_mode='html')


def register_handlers_revise(dp: Dispatcher):
	dp.register_message_handler(revise, commands="revise", state="*")
	dp.register_message_handler(revise, CommandStart(deep_link="revise"), state="*")
	dp.register_message_handler(entered_date, state=ReviseStates.add_date)
	dp.register_message_handler(archive, Text(equals="Архів", ignore_case=True), state=ReviseStates.inactive)
	dp.register_message_handler(all_period, Text(equals="Увесь час", ignore_case=True), state=ReviseStates.inactive)
