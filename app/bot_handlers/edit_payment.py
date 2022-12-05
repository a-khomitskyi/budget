from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters.builtin import CommandStart
from datetime import datetime
import db_config


class ActionStates(StatesGroup):
	set_edit = State()
	set_delete = State()
	set_inactive = State()


class AddStates(StatesGroup):
	add_title = State()
	add_price = State()


async def show_last_row(message: types.Message, state: FSMContext):
	row_data = db_config.get_last_records(db_config.create_conn_psc2(), message.chat.id, message.from_user.id)
	if not row_data:
		await message.answer("Статистики ще не існує ...")
	else:
		msg = ""
		pid_list = []

		for i in row_data:
			tmp = i[0].replace('(', '').replace(')', '').split(',')
			tmp[2] = datetime.fromisoformat(tmp[2].replace('"', '')).strftime('%d-%m-%Y')
			msg += f"<code><b>{tmp[0]}</b></code>📌️ <i>{tmp[2]}</i> <code>[{tmp[1]}]</code> — <b>{tmp[4]} грн</b> 👉 {tmp[3]}\n"

			pid_list.append(tmp[0])

		await state.update_data(pid_list=pid_list)
		await message.answer(msg, parse_mode='html')

		keyboard = types.InlineKeyboardMarkup()
		buttons = [
			types.InlineKeyboardButton(text="Редагувати", callback_data="edit_row"),
			types.InlineKeyboardButton(text="Видалити", callback_data="delete_row")
		]
		keyboard.add(*buttons)
		await message.answer("Оберіть дію 👇", reply_markup=keyboard)


async def get_action(call: types.CallbackQuery):
	match call.data:
		case "edit_row":
			await ActionStates.set_edit.set()
			await call.answer("Який запис хочете редагувати?")
		case "delete_row":
			await ActionStates.set_delete.set()
			await call.answer("Який запис хочете видалити?")


async def edit_payment(message: types.Message, state: FSMContext):
	user_data = await state.get_data()

	if not int(message.text) not in user_data['pid_list']:
		await message.reply("Не можливо редагувати! Вкажіть вірне значення")
		return

	await state.update_data(pid=int(message.text))
	await message.answer("O'key, редагуємо 👇")
	await message.answer('Вкажіть назву товару:')
	await ActionStates.set_inactive.set()
	await AddStates.add_title.set()


async def title_added(message: types.Message, state: FSMContext):
	await state.update_data(title=message.text.strip())
	await message.answer("Скільки витратили?")
	await AddStates.add_price.set()


async def price_added(message: types.Message, state: FSMContext):
	if not message.text.strip().replace('.', '', 1).isdigit() or message.text.strip().replace(',', '', 1).isdigit():
		await message.reply("Тут зайві символи, введіть суму ще раз:")
		return

	user_data = await state.get_data()

	# Save to DB new order
	db_config.save_payment(db_config.create_conn_psc2(), [user_data['title'], message.text.strip(), user_data['pid']])

	await message.answer("Готово!")
	await state.finish()


async def delete_payment(message: types.Message, state: FSMContext):
	user_data = await state.get_data()

	if not int(message.text) not in user_data['pid_list']:
		await message.reply("Не можливо видалити! Вкажіть вірне значення")
		return

	db_config.delete_payment(db_config.create_conn_psc2(), user_data['pid'])
	await message.answer(f"O'key, запис #{message.text} видалено")
	await state.finish()


def register_handlers_edit(dp: Dispatcher):
	dp.register_message_handler(show_last_row, commands="edit", state="*")
	dp.register_message_handler(show_last_row, CommandStart(deep_link="edit"), state="*")
	dp.callback_query_handler(get_action, lambda call: call.data == 'delete_row', state="*")
	dp.callback_query_handler(get_action, lambda call: call.data == 'edit_row', state="*")
	dp.register_message_handler(edit_payment, state=ActionStates.set_edit)
	dp.register_message_handler(delete_payment, state=ActionStates.set_delete)
	dp.register_message_handler(title_added, state=AddStates.add_title)
	dp.register_message_handler(price_added, state=AddStates.add_price)
# dp.register_callback_query_handler(text='edit_row', state="*")
# dp.register_callback_query_handler(text='delete_row')
# dp.register_message_handler(get_last_rows, Text(equals="додати", ignore_case=True), state="*")
# dp.register_message_handler(title_added, state=AddStates.add_title)
# dp.register_message_handler(price_added, state=AddStates.add_price)
