import aiogram
import configparser


config = configparser.ConfigParser()
config.read('bot_info.ini')
config.sections()
TOKEN = config["BOT"]["token"]

bot = aiogram.Bot(token=TOKEN)
dp = aiogram.Dispatcher(bot)

if __name__ == "__main__":
    pass
