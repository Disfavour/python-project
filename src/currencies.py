"""Валюты."""

import aiogram
import requests
import os
import gettext
from stuff import get_inline_keyboard_from_list

gettext.install("telbot", os.path.dirname(__file__))

CHOICE = [_("Конвертер валют"), _("Курс Валют")]

CURRENCIES_FROM = [_("RUB (Рубль)"), _("EUR (Евро)"), _("USD (Доллар)"), _("GBP (Фунт стерлингов)"),
                   _("CNY (Китайский Юань)"), _("CHF (Швейцарский франк)"), _("BYN (Белорусский рубль)")]
CURRENCIES_TO = [_("в RUB (Рубль)"), _("в EUR (Евро)"), _("в USD (Доллар)"), _("в GBP (Фунт стерлингов)"),
                 _("в CNY (Китайский Юань)"), _("в CHF (Швейцарский франк)"), _("в BYN (Белорусский рубль)")]
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
    await message.answer(text=_("Выберите функцию"), reply_markup=get_inline_keyboard_from_list(CHOICE))


async def currency_handle_callback(call: aiogram.types.CallbackQuery):
    """
    Обработка нажатия на кнопки встроенной клавиатуры.

    :param call: вызов бота
    """
    choice = call.data
    if choice == _("Конвертер валют"):
        await call.message.answer(
            text=_("Выберите валюту, из которой нужно перевести"),
            reply_markup=get_inline_keyboard_from_list(CURRENCIES_FROM))
    elif choice == _("Курс Валют"):
        for i in CURRENCIES_FROM[1:]:
            res = Exchange(1).exchange(i.split()[0], "RUB")
            await call.message.answer("1 {} = {} RUB".format(i, res), parse_mode=aiogram.types.ParseMode.HTML)


async def exchange_currency_handle_callback(call: aiogram.types.CallbackQuery):
    """
    Обработка нажатия на кнопки встроенной клавиатуры.

    :param call: вызов бота
    """
    global cur1
    cur1 = call.data.split()[0]
    await call.message.edit_text(
        text=_("Выберите валюту, в которую нужно перевести"),
        reply_markup=get_inline_keyboard_from_list(CURRENCIES_TO))


async def amount_currency_handle_callback(call: aiogram.types.CallbackQuery):
    """
    Ввод с клавиатуры.

    :param call: вызов бота
    """
    global cur1, cur2
    cur2 = call.data.split()[1]
    await call.message.answer(text=_("Какую сумму перевести?"), parse_mode=aiogram.types.ParseMode.HTML)


async def return_exchange_handle_callback(message: aiogram.types.Message):
    """
    Окончательный ответ на запрос конвертера валют.

    :param message: вызов бота
    """
    res = Exchange(message.text).exchange(cur1, cur2)
    await message.answer(text="{} -> {}: {}".format(cur1, cur2, res), parse_mode=aiogram.types.ParseMode.HTML)


def register_handlers(dp: aiogram.Dispatcher) -> None:
    """
    Зарегистрировать обработчики.

    :param dp: диспетчер бота
    """
    dp.register_message_handler(currency_handler, regexp=_(r"^Валюты"))
    dp.register_callback_query_handler(currency_handle_callback, text=CHOICE)
    dp.register_callback_query_handler(exchange_currency_handle_callback, text=CURRENCIES_FROM)
    dp.register_callback_query_handler(amount_currency_handle_callback, text=CURRENCIES_TO)
    dp.register_message_handler(return_exchange_handle_callback, regexp=r"^\d+$")
