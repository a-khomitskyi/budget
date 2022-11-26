from enum import Enum

db_file = "database.vdb"


class States(Enum):
	"""
	Мы используем БД Vedis, в которой хранимые значения всегда строки,
	поэтому и тут будем использовать тоже строки (str)
	"""
	S_START = "0"  # Начало нового диалога
	S_CHOICE = "1"
