import aiogram
import stuff
import parsing


horoscope_obj = parsing.HOROSCOPE()


async def horoscope(message: aiogram.types.Message):
    """Показать все знаки гороскопа."""
    signs = horoscope_obj.get_signs()
    await message.answer("Выберите ваш знак зодиака", reply_markup=stuff.get_inline_keyboard_from_list(signs))


async def handle_horoscope_callback(call: aiogram.types.CallbackQuery):
    sign = call.data
    text = horoscope_obj.get_data_smart(sign)
    await call.message.edit_text(text, parse_mode=aiogram.types.ParseMode.HTML)
    await call.answer()


def register_handlers(dp: aiogram.Dispatcher) -> None:
    dp.register_message_handler(horoscope, regexp=r"^Гороскоп$")
    dp.register_callback_query_handler(handle_horoscope_callback, text=horoscope_obj.get_signs())


if __name__ == "__main__":
    pass
