"""Валюты."""

import aiogram
import requests
from .stuff import get_inline_keyboard_from_list

CHOICE = ["Конвертер валют", "Курс Валют"]

CURRENCIES_FROM = ["RUB", "EUR", "USD", "GBP", "CNY", "CHF", "BYN"]
CURRENCIES_TO = ["в RUB", "в EUR", "в USD", "в GBP", "в CNY", "в CHF", "в BYN"]
cur1, cur2 = '', ''


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
        self.amount = int(amount)
        self.bank_link = self.bank(Currency.link)

    def exchange(self, cur_from, cur_to):
        """Перевод из валюты cur1 в cur2."""
        lst = [cur_to, cur_from]
        for i, j in enumerate(lst):
            if j != "RUB":
                lst[i] = self.bank_link[j]['Value']
            else:
                lst[i] = 1
        return lst[1] * self.amount / lst[0]


async def currency_handler(message: aiogram.types.Message):
    """
    Обработка нажатия на кнопку 'Валюты'.

    :param message: сообщение для бота
    """
    await message.answer(text="Выберите функцию", reply_markup=get_inline_keyboard_from_list(CHOICE))


async def currency_handle_callback(call: aiogram.types.CallbackQuery):
    """
    Обработка нажатия на кнопки встроенной клавиатуры.

    :param call: вызов бота
    """
    print('currency_handle_callback')
    choice = call.data
    if choice == "Конвертер валют":
        await call.message.answer(
            text="Выберите валюту, из которой нужно перевести",
            reply_markup=get_inline_keyboard_from_list(CURRENCIES_FROM))
    elif choice == "Курс Валют":
        for i in CURRENCIES_FROM[1:]:
            res = Exchange(1).exchange("RUB", i)
            await call.message.answer("RUB -> {}: {}".format(i, res), parse_mode=aiogram.types.ParseMode.HTML)


async def exchange_currency_handle_callback(call: aiogram.types.CallbackQuery):
    """
    Обработка нажатия на кнопки встроенной клавиатуры.

    :param call: вызов бота
    """
    print('exchange_currency_handle_callback')
    global cur1
    cur1 = call.data
    await call.message.edit_text(
        text="Выберите валюту, в которую нужно перевести",
        reply_markup=get_inline_keyboard_from_list(CURRENCIES_TO))


async def amount_currency_handle_callback(call: aiogram.types.CallbackQuery):
    """
    Ввод с клавиатуры.

    :param call: вызов бота
    """
    print('amount_currency_handle_callback')
    global cur1, cur2
    cur2 = call.data.split()[1]
    print(cur1, cur2)
    await call.message.answer(text="Какую сумму перевести?", parse_mode=aiogram.types.ParseMode.HTML)


async def return_exchange_handle_callback(message: aiogram.types.Message):
    """
    Окончательный ответ на запрос конвертера валют.

    :param call: вызов бота
    """
    print('return_exchange_handle_callback')
    res = Exchange(message.text).exchange(cur1, cur2)
    print(res)
    await message.answer(text=res, parse_mode=aiogram.types.ParseMode.HTML)


def register_handlers(dp: aiogram.Dispatcher) -> None:
    """
    Зарегистрировать обработчики.

    :param dp: диспетчер бота
    """
    dp.register_message_handler(currency_handler, regexp=r"^Валюты")
    dp.register_callback_query_handler(currency_handle_callback, text=CHOICE)
    dp.register_callback_query_handler(exchange_currency_handle_callback, text=CURRENCIES_FROM)
    dp.register_callback_query_handler(amount_currency_handle_callback, text=CURRENCIES_TO)
    dp.register_message_handler(return_exchange_handle_callback, regexp=r"^\d+$")
