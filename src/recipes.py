"""Обработка кулинарных рецептов."""

import aiogram
import random
import aiogram.utils.markdown as fmt
import os
import gettext

import database
from stuff import get_inline_keyboard_from_list, get_more_inline_keyboard
from stuff import get_another_inline_keyboard

gettext.install("telbot", os.path.dirname(__file__))


CHOICE = [_("Любой"), _("По ингредиентам")]
NEXT = _("Следующий")
RECIPES_LIST = []
CNT = 0


def form_answer(recipe: dict) -> str:
    """
    Оформить данные о рецепте в виде, удобном для вывода в чат с пользователем.

    :param recipe: данные рецепта
    """
    ingr = ""
    for num, item in enumerate(recipe["ingrs"]):
        ingr += f"{num+1}) {item}\n"
    return fmt.text(
        fmt.text(fmt.hbold(recipe["name"])),
        fmt.text("Ингредиенты:\n", ingr),
        fmt.hlink(recipe["name"], recipe["link"]),
        sep="\n"
    )


async def recipes_handler(message: aiogram.types.Message):
    """
    Обработка нажатия на кнопку 'Кулинарные рецепты'.

    :param message: сообщение для бота
    """
    await message.answer(
        fmt.text(_("Нужен рецепт с определенными ингредиентами или любой?")),
        reply_markup=get_inline_keyboard_from_list(CHOICE))


async def recipes_handle_callback(call: aiogram.types.CallbackQuery):
    """
    Обработка нажатия на кнопки встроенной клавиатуры.

    :param call: вызов бота
    """
    choice = call.data
    if choice == _("Любой"):
        cur_recipe = database.fetch_by_id(random.randint(1, 4497))[0]
        await call.message.answer(
            form_answer(cur_recipe[1]),
            parse_mode=aiogram.types.ParseMode.HTML,
            reply_markup=get_more_inline_keyboard(choice))
    elif choice == _("По ингредиентам"):
        await call.message.answer(
            fmt.text(
                _("Введите ингредиенты с большой буквы через запятую, ") +
                _("начиная со слова 'Ингредиенты:'\n Пример: \n") +
                _("'Ингредиенты:  Вишня, Корица, Сахар'\n") +
                _("По возможности уточняйте название ингредиента: ") +
                _("вместо 'Перец' введите 'Перец черный' и т.п.")),
            parse_mode=aiogram.types.ParseMode.HTML)


async def recipes_handle_ingreds(message: aiogram.types.Message):
    """
    Найти рецепты, содержащие нужные ингредиенты.

    Найденные рецепты сохраняются, выводится первый.
    :param message: сообщение боту
    """
    ingreds = message.text
    ingreds = ingreds.split(":")[1].split(",")
    for k, ingr in enumerate(ingreds):
        while ingr[0].isspace():
            ingr = ingr[1:]
        while ingr[-1].isspace():
            ingr = ingr[:-1]
        ingreds[k] = ingr
    global CNT, RECIPES_LIST
    RECIPES_LIST = database.fetch_by_ingreds(ingreds)
    CNT = 0
    if len(RECIPES_LIST) != 0:
        await message.answer(
            form_answer(RECIPES_LIST[CNT][1]),
            parse_mode=aiogram.types.ParseMode.HTML,
            reply_markup=get_another_inline_keyboard(NEXT))
    else:
        await message.answer(
            fmt.text(_("Нет рецептов с таким набором ингредиентов.")),
            parse_mode=aiogram.types.ParseMode.HTML)


async def recipes_handle_ingreds_callback(call: aiogram.types.CallbackQuery):
    """
    Вывести следующий рецепт с нужными ингредиентами.

    :param call: вызов бота
    """
    global CNT, RECIPES_LIST
    CNT += 1
    if CNT < len(RECIPES_LIST):
        await call.message.answer(
            form_answer(RECIPES_LIST[CNT][1]),
            parse_mode=aiogram.types.ParseMode.HTML,
            reply_markup=get_another_inline_keyboard(call.data))
    else:
        await call.message.answer(
            fmt.text(_("Рецепты с такими ингредиентами закончились.")),
            parse_mode=aiogram.types.ParseMode.HTML)


def register_handlers(dp: aiogram.Dispatcher) -> None:
    """
    Зарегистрировать обработчики.

    :param dp: диспетчер бота
    """
    dp.register_message_handler(recipes_handler, regexp=_(r"^Кулинарные рецепты$"))
    dp.register_callback_query_handler(recipes_handle_callback, text=CHOICE)
    dp.register_message_handler(recipes_handle_ingreds, regexp=(r"Ингредиенты:(.)*"))
    dp.register_callback_query_handler(recipes_handle_ingreds_callback, text=NEXT)
