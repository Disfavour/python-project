"""Списки покупок."""

import aiogram
import aiogram.utils.markdown as fmt
import database
from stuff import get_inline_keyboard_from_list, get_more_inline_keyboard
from stuff import get_another_inline_keyboard

CHOICE_MAIN = ["Добавить новый список", "Просмотреть лист списков", "Очистить лист списков"]


def list_print(shoplist: list) -> str:
    """
    Оформить данные о списке в виде, удобном для вывода в чат с пользователем.

    :param shoplist: данные списка покупок
    """
    out = ""
    for i in range(len(shoplist)):
        out += shoplist[i][2]["name"] + ":\n"
        lst = shoplist[i][2]["shopping_list"].split(',')
        for j in range(len(lst)):
            out += f"{j + 1}. {lst[j]}\n"
        out += '\n'
    return out


async def shopping_lists_handler(message: aiogram.types.Message):
    """
    Обработка нажатия на кнопку 'Списки покупок'.

    :param message: сообщение для бота
    """
    await message.answer(
        fmt.text("Выберите интересующее действие."),
        reply_markup=get_inline_keyboard_from_list(CHOICE_MAIN))


async def shopping_lists_handle_callback(call: aiogram.types.CallbackQuery):
    """
    Обработка нажатия на кнопки встроенной клавиатуры.

    :param call: вызов бота
    """
    choice = call.data
    if choice == "Добавить новый список":
        await call.message.answer(fmt.text("Введите пункты списка через запятую, начиная со слов:\n" +
                                           "Список *Название:*\n" +
                                           "Пример: \nСписок *Повседневный*: Хлеб, Молоко (2 литра), " +
                                           "Сахар, Бумажные полотенца"), parse_mode=aiogram.types.ParseMode.HTML)
    elif choice == "Просмотреть лист списков":
        s = list_print(database.take_all())
        if s:
            await call.message.answer(
                s,
                parse_mode=aiogram.types.ParseMode.HTML)
        else:
            await call.message.answer(
                "В базе данных нет доступных списков",
                parse_mode=aiogram.types.ParseMode.HTML)
    elif choice == "Очистить лист списков":
        database.delete_table_data("shopping_lists")
        await call.message.answer(
            "Очистка произведена успешно",
            parse_mode=aiogram.types.ParseMode.HTML)


async def shopping_handle_lists(message: aiogram.types.Message):
    """
    Сохранение списка.

    :param message: сообщение боту
    """
    shopping_lists = message.text
    name = shopping_lists.split("*")[1]
    shopping_list = shopping_lists.split(":")[1]
    data = dict()
    for i in ("name", "shopping_list"):
        data[i] = ''
    data['name'] = name
    data['shopping_list'] = shopping_list
    database.add_line(data, "shopping_lists")


def register_handlers(dp: aiogram.Dispatcher) -> None:
    """
    Зарегистрировать обработчики.

    :param dp: диспетчер бота
    """
    dp.register_message_handler(shopping_lists_handler, regexp=r"^Списки покупок$")
    dp.register_callback_query_handler(shopping_lists_handle_callback, text=CHOICE_MAIN)
    dp.register_message_handler(shopping_handle_lists, regexp=r"Список(.)*")
