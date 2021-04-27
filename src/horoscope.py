import aiogram
from bot import dp


zodiac_signs = ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", "Весы",
                "Скорпион", "Змееносец", "Стрелец", "Козерог", "Водолей", "Рыбы"]


def get_keyboard_from_list(items):
    keyboard = aiogram.types.InlineKeyboardMarkup()
    tmp = []
    for item in items:
        tmp.append(aiogram.types.InlineKeyboardButton(text=item, callback_data=item))
    keyboard.add(*tmp)
    return keyboard


@dp.message_handler(regexp=r"^Гороскоп$")
async def horoscope(message: aiogram.types.Message):
    """Показать все знаки гороскопа."""
    await message.answer("Выберите ваш знак зодиака", reply_markup=get_keyboard_from_list(zodiac_signs))


@dp.callback_query_handler(text=zodiac_signs)
async def send_random_value(call: aiogram.types.CallbackQuery):
    await call.message.answer(call.data)


if __name__ == "__main__":
    pass
