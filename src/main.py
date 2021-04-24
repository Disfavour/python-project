import aiogram
from aiogram.utils.exceptions import BotBlocked


bot = aiogram.Bot(token="1796535419:AAFMLfG35KAugeQqhDmWdApx5pZMnK43fDU")
dp = aiogram.Dispatcher(bot)


@dp.message_handler()
async def echo(message: aiogram.types.Message):
    await message.answer(message.text)


@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: aiogram.types.Update, exception: BotBlocked):
    """Если заблокировали бота."""
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")
    return True


if __name__ == "__main__":
    aiogram.executor.start_polling(dp, skip_updates=True)
