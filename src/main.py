"""Телеграм бот."""
import aiogram
from aiogram.utils.exceptions import BotBlocked

import afisha
import bot
import horoscope
import news
import recipes
import reminder
import stuff
import weather


async def get_help(message: aiogram.types.Message):
    """
    Показать помощь.

    :param message: сообщение
    """
    keyboard = aiogram.types.InlineKeyboardMarkup()
    keyboard.add(aiogram.types.InlineKeyboardButton(text="Проект", url="https://github.com/Disfavour/python-project"))
    await message.reply("Документацию можно найти здесь", reply_markup=keyboard)


async def cmd_start(message: aiogram.types.Message):
    """
    Предоставить выбор функции.

    :param message: сообщение
    """
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = stuff.base_options
    keyboard.add(*buttons)
    await message.reply("Выберите функцию", reply_markup=keyboard)


async def cmd_dice(message: aiogram.types.Message):
    """
    Показать бросание кубика.

    :param message: сообщение
    """
    await message.reply_dice(emoji="🎲")


async def echo(message: aiogram.types.Message):
    """
    Показать, что команда не распознана.

    :param message: сообщение
    """
    await message.reply("Не распознано '" + message.text + "'")


async def error_bot_blocked(update: aiogram.types.Update, exception: BotBlocked):
    """
    Обработать блокирование бота.

    :param update: входящее обновление
    :param exception: исключение
    """
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")
    return True


class REGISTRATION:
    """
    Класс регистрации и начала работы.

    :param dp: диспетчер
    """

    def __init__(self, dp):
        """Инициализировать диспетчер."""
        self.dp = dp

    def start(self) -> None:
        """Зарегестрировать обработчики и начать работу."""
        self.register_handlers()
        aiogram.executor.start_polling(self.dp, skip_updates=True)

    def register_handlers(self) -> None:
        """Зарегестрировать обработчики."""
        horoscope.register_handlers(self.dp)
        news.register_handlers(self.dp)
        weather.register_handlers(self.dp)
        afisha.register_handlers(self.dp)
        recipes.register_handlers(self.dp)
        reminder.register_handlers(self.dp)

        # Это последнее, иначе эхо-обработчик перебьёт другие.
        self.register_base_handlers()

    def register_base_handlers(self) -> None:
        """Зарегестрировать базовые обработчики."""
        self.dp.register_message_handler(get_help, commands="help")
        self.dp.register_message_handler(cmd_start, commands="start")
        self.dp.register_message_handler(cmd_dice, commands="dice")
        self.dp.register_message_handler(echo)
        self.dp.register_errors_handler(error_bot_blocked, exception=BotBlocked)


if __name__ == "__main__":
    obj = REGISTRATION(bot.dp)
    obj.start()
