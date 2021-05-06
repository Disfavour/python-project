import aiogram
from bot import dp
from aiogram.utils.callback_data import CallbackData
import parsing


callback_horoscope = CallbackData("horoscope", "url")


@dp.message_handler(regexp=r"^Гороскоп$")
async def horoscope(message: aiogram.types.Message):
    """Показать все знаки гороскопа."""
    d = parsing.get_horoscope_signs()
    keyboard = aiogram.types.InlineKeyboardMarkup()
    tmp = []
    for key, value in d.items():
        tmp.append(aiogram.types.InlineKeyboardButton(
            text=key, callback_data=callback_horoscope.new(url=value)))
    keyboard.add(*tmp)
    await message.answer("Выберите ваш знак зодиака", reply_markup=keyboard)


@dp.callback_query_handler(callback_horoscope.filter())
async def handle_horoscope_callback(call: aiogram.types.CallbackQuery, callback_data: dict):
    url = callback_data["url"]
    text = parsing.parse_horoscope_sign(url)
    await call.message.edit_text(text)
    await call.answer()


if __name__ == "__main__":
    pass
