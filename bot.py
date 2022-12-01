from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.bot_handlers.default import register_handlers_dafault
from app.bot_handlers.add_payment import register_handlers_add
# from app.bot_handlers.edit_payment import register_handlers_edit
from app.bot_handlers.statistic_payments import register_handlers_stat
# from app.bot_handlers.revise_payments import register_handlers_revise

from os import getenv
from dotenv import load_dotenv
import logging
import asyncio

logger = logging.getLogger(__name__)
load_dotenv()


# Command registration
async def set_commands(bot: Bot):
	commands = [
		BotCommand(command="/start", description="Додати покупку в список"),
		BotCommand(command="/add", description="Додати покупку в список"),
		BotCommand(command="/stat", description=" Вивести статистику витрат за поточний місяць"),
		BotCommand(command="/edit", description="Редагувати додану покупку"),
		BotCommand(command="/revise", description=" Вивести статистику витрат помісячно за поточний рік"),
		BotCommand(command="/help", description="Інформація про бота")
	]
	await bot.set_my_commands(commands)


async def main():
	# Setting logging in stdout
	logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(name)s] - %(message)s', datefmt='%H:%M:%S')
	logger.error("Starting bot")

	# Initializing bot
	bot = Bot(getenv("TOKEN"))
	dp = Dispatcher(bot, storage=MemoryStorage())

	# Handlers registration
	register_handlers_dafault(dp)
	register_handlers_add(dp)
	register_handlers_stat(dp)
	# register_handlers_stat(dp)
	# register_handlers_edit(dp)
	# register_handlers_revise(dp)
	# register_handlers_help(dp)

	# Setting-up bot
	await set_commands(bot)
	await dp.skip_updates()  # skip updates pull (optionally)
	await dp.start_polling()


if __name__ == '__main__':
	asyncio.run(main())
