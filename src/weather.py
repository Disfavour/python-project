"""Обработка погоды."""
import aiogram
import os
import gettext

import parsing

gettext.install("telbot", os.path.dirname(__file__))


weather_obj = parsing.WEATHER()


async def weather_handle(message: aiogram.types.Message):
    """
    Показать погоду.

    :param message: сообщение
    """
    text = weather_obj.get_data_smart()
    await message.answer(text, parse_mode=aiogram.types.ParseMode.HTML)


def register_handlers(dp: aiogram.Dispatcher) -> None:
    """
    Зарегистрировать обработчики.

    :param dp: диспетчер
    """
    dp.register_message_handler(weather_handle, regexp=_(r"^Погода$"))


if __name__ == "__main__":
    pass
