from telegrask import Telegrask
from tinydb import TinyDB
from .config import TOKEN, DB_PATH

bot = Telegrask(TOKEN)
db = TinyDB(DB_PATH)

from . import commands
