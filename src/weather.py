import aiogram
from bot import dp
import parsing
import aiogram.utils.markdown as fmt


@dp.message_handler(regexp=r"^Погода$")
async def horoscope(message: aiogram.types.Message):
    """Показать все знаки гороскопа."""
    info, d = parsing.parse_weather()
    keyboard = aiogram.types.InlineKeyboardMarkup()
    keyboard.add(aiogram.types.InlineKeyboardButton(text="Погода", url=parsing.url_weather))
    await message.answer("Новости:"+ str(info)+ str(d), reply_markup=keyboard)


if __name__ == "__main__":
    pass
