"""Обработка гороскопа."""
import aiogram
import stuff
import parsing
import os
import gettext

gettext.install("telbot", os.path.dirname(__file__))


horoscope_obj = parsing.HOROSCOPE()


async def horoscope_handle(message: aiogram.types.Message):
    """
    Предоставить выбор знака зодиака.

    :param message: сообщение
    """
    signs = horoscope_obj.get_signs()
    await message.answer(_("Выберите ваш знак зодиака"), reply_markup=stuff.get_inline_keyboard_from_list(signs))


async def horoscope_handle_callback(call: aiogram.types.CallbackQuery):
    """
    Обработать нажатие кнопки.

    :param call: вызов
    """
    sign = call.data
    text = horoscope_obj.get_data_smart(sign)
    await call.message.edit_text(text, parse_mode=aiogram.types.ParseMode.HTML)
    await call.answer()


def register_handlers(dp: aiogram.Dispatcher) -> None:
    """
    Зарегистрировать обработчики.

    :param dp: диспетчер
    """
    dp.register_message_handler(horoscope_handle, regexp=_(r"^Гороскоп$"))
    dp.register_callback_query_handler(horoscope_handle_callback, text=horoscope_obj.get_signs())


if __name__ == "__main__":
    pass
