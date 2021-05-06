import aiogram
from bot import dp
from aiogram.utils.callback_data import CallbackData
import parsing


callback_news = CallbackData("news", "count")


@dp.message_handler(regexp=r"^Новости$")
async def horoscope(message: aiogram.types.Message):
    """Показать все знаки гороскопа."""
    keyboard = aiogram.types.InlineKeyboardMarkup()
    d = parsing.parse_news()
    for number, (key, value) in enumerate(d.items()):
        if number < 10:
            keyboard.add(
                aiogram.types.InlineKeyboardButton(text=key, url=parsing.url_news_part + value))
    keyboard.add(aiogram.types.InlineKeyboardButton(text="Ещё", callback_data=callback_news.new(count=1)))
    await message.answer("Новости:", reply_markup=keyboard)


@dp.callback_query_handler(callback_news.filter())
async def handle_news_callback(call: aiogram.types.CallbackQuery, callback_data: dict):
    keyboard = aiogram.types.InlineKeyboardMarkup()
    d = parsing.parse_news()
    for number, (key, value) in enumerate(d.items()):
        if number > 10:
            keyboard.add(
                aiogram.types.InlineKeyboardButton(text=key, url=parsing.url_news_part + value))
    await call.message.edit_reply_markup(reply_markup=keyboard)
    await call.answer()


if __name__ == "__main__":
    pass
