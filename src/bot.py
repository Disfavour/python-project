"""Объект бота."""
import aiogram
import configparser
import os


config = configparser.ConfigParser()
config.read(os.path.dirname(__file__) + "/bot_info.ini")
config.sections()
TOKEN = config["BOT"]["token"]

bot = aiogram.Bot(token=TOKEN)
dp = aiogram.Dispatcher(bot)

if __name__ == "__main__":
    pass
