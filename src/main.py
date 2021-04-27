from aiogram.utils.exceptions import BotBlocked
from horoscope import *


options = ["Гороскоп", "Погода", "Новости",
           "Напоминания", "Счётчик расходов/доходов", "Списки покупок",
           "Список ближайших премьер", "Рецепты по ингредиентам"]


@dp.message_handler(commands="help")
async def get_help(message: aiogram.types.Message):
    """Получить помощь."""
    keyboard = aiogram.types.InlineKeyboardMarkup()
    keyboard.add(aiogram.types.InlineKeyboardButton(text="Проект", url="https://github.com/Disfavour/python-project"))
    await message.reply("/help\n"
                        "/dice\n"
                        "/start",
                        reply_markup=keyboard)


@dp.message_handler(commands="start")
async def cmd_start(message: aiogram.types.Message):
    """Показать функции пользователю."""
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = options
    keyboard.add(*buttons)
    await message.answer("Выберите функцию", reply_markup=keyboard)


@dp.message_handler(commands="dice")
async def cmd_dice(message: aiogram.types.Message):
    """Кинуть кубик."""
    await message.answer_dice(emoji="🎲")


@dp.message_handler()
async def echo(message: aiogram.types.Message):
    """Не распознаная команда."""
    await message.answer("Не распознано '" + message.text + "'")


@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: aiogram.types.Update, exception: BotBlocked):
    """Если заблокировали бота."""
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")
    return True


if __name__ == "__main__":
    aiogram.executor.start_polling(dp, skip_updates=True)
