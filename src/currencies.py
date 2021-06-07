"""Валюты."""

import aiogram

from stuff import get_inline_keyboard_from_list

CHOICE = ["Конвертер валют", "Курс Валют"]


async def currency_handler(message: aiogram.types.Message):
    """
    Обработка нажатия на кнопку 'Кулинарные рецепты'.

    :param message: сообщение для бота
    """
    await message.answer(text="Выберите функцию", reply_markup=get_inline_keyboard_from_list(CHOICE))


async def currency_handle_callback(call: aiogram.types.CallbackQuery):
    """
    Обработка нажатия на кнопки встроенной клавиатуры.

    :param call: вызов бота
    """
    choice = call.data
    if choice == "Конвертер валют":
        """Обработка конвертера валют"""
    elif choice == "Курс Валют":
        """Обработка курса валют"""


def register_handlers(dp: aiogram.Dispatcher) -> None:
    """
    Зарегистрировать обработчики.

    :param dp: диспетчер бота
    """
    dp.register_message_handler(currency_handler, regexp=r"^Валюты")
    dp.register_callback_query_handler(currency_handle_callback, text=CHOICE)
