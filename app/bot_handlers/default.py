from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


async def cmd_start(message: types.Message, state: FSMContext):
	await state.finish()
	await message.answer(
		f"<b>Привіт, {message.from_user.full_name}</b>!\n\nЯ Бот, що займається підрахунком витрат. Ось основиний перелік того, що я вмію:\n<code>/add</code> — Додати покупку в список;\n<code>/stat</code> — Вивести статистику витрат за поточний місяць;\n<code>/revise</code> — Вивести статистику витрат помісячно за поточний рік;\n<code>/edit</code> — Редагувати додану покупку\n<code>/help</code> — Інформація щодо бота\n\nНумо починати!",
		parse_mode='html')


async def cmd_cancel(message: types.Message, state: FSMContext):
	await state.finish()
	await message.answer("Дія скасована")


def register_handlers_dafault(dp: Dispatcher):
	dp.register_message_handler(cmd_start, commands=["start", "help"], state="*")
	dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
	dp.register_message_handler(cmd_cancel, Text(equals="скасувати", ignore_case=True), state="*")
