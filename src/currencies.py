"""Валюты."""

import aiogram
import requests

from stuff import get_inline_keyboard_from_list

CHOICE = ["Конвертер валют", "Курс Валют"]

CURRENCIES = ["RUB", "EUR", "USD", "GBP", "CNY", "CHF", "BYN"]


class Currency:
    """Класс валют."""

    link = "https://www.cbr-xml-daily.ru/daily_json.js"

    def bank(self, link):
        """подключение к таблице с данными по курсу."""
        link = Currency.link
        data = requests.get(link)
        forex = data.json()['Valute']
        return forex


class Exchange(Currency):
    """Класс перевода валют."""

    def __init__(self, amount):
        """Инициализировать перевод валют."""
        self.amount = amount
        self.bank_link = self.bank(Currency.link)

    def exchange(self, cur1, cur2):
        """Перевод из валюты cur1 в cur2."""
        lst = [cur1, cur2]
        for i, j in enumerate(lst):
            if j != "RUB":
                lst[i] = self.bank_link[j]['Value']
            else:
                lst[i] = 1
        return lst[1] * self.amount / lst[0]


Exchange(1).exchange("RUB", "USD")


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
        await call.message.answer(
            text="Выберите валюту, из которой нужно перевести",
            reply_markup=get_inline_keyboard_from_list(CURRENCIES))
    elif choice == "Курс Валют":
        for i in CURRENCIES[1:]:
            res = Exchange(1).exchange("RUB", i)
            await call.message.answer("RUB -> {}: {}".format(i, res), parse_mode=aiogram.types.ParseMode.HTML)


def register_handlers(dp: aiogram.Dispatcher) -> None:
    """
    Зарегистрировать обработчики.

    :param dp: диспетчер бота
    """
    dp.register_message_handler(currency_handler, regexp=r"^Валюты")
    dp.register_callback_query_handler(currency_handle_callback, text=CHOICE)
