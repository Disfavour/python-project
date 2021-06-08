"""Обработка напоминаний."""
import asyncio

import aiocron
import aiogram
import aiogram.utils.markdown as fmt
import nest_asyncio
import database
from stuff import get_inline_keyboard_from_list

CHOICES = ["День Рождения", "ЖКХ", "Мобильная Связь", "Планер", "Подписки", "Приём Лекарств", "Удалить"]
YESNO = ["Да", "Нет"]
choice = ""
nest_asyncio.apply()


async def reminder_handle(message: aiogram.types.Message):
    """
    Предоставить выбор типа напоминания.

    :param message: сообщение
    """
    await message.answer("Выберите тип напоминания",
                         reply_markup=get_inline_keyboard_from_list(CHOICES))

    @aiocron.crontab('* * * * *')
    async def crontab():
        await at_time(message)
    asyncio.get_event_loop().run_forever()


async def at_time(message: aiogram.types.Message):
    """
    Проверка на наличие напоминания в этот день и время.

    :param message: сообщение
    """
    try:
        for j in CHOICES[:-1]:
            res = database.get_line_notif(j)
            print("res:", res)
            for i in res:
                if i is not None:
                    notif = 'Напоминание: {} – {} {} {}'.format(i[-1], i[1], i[2], i[3])
                    await message.answer(notif, parse_mode=aiogram.types.ParseMode.HTML)
    except Exception as error:
        print(error)


async def reminder_handle_callback(call: aiogram.types.CallbackQuery):
    """
    Обработка нажатия на кнопки встроенной клавиатуры.

    :param call: вызов бота
    """
    global choice
    choice = call.data
    if choice == "День Рождения":
        await call.message.answer(fmt.text("Введите ФИО, день рождения именинника в формате:\n" +
                                           "и время напоминания в формате\n" +
                                           "Напоминание: Фамилия Имя Отчество дд.мм чч:мм\n" +
                                           "Например:\nНапоминание: Иванов Иван Иванович 11.12 13:14"),
                                  parse_mode=aiogram.types.ParseMode.HTML)
    elif choice == "ЖКХ":
        await call.message.answer(fmt.text("Введите дату оплаты ЖКХ и время напоминания в формате\n" +
                                           "Напоминание: дд чч:мм\n" +
                                           "Например:\nНапоминание: 17 18:19"),
                                  parse_mode=aiogram.types.ParseMode.HTML)
    elif choice == "Мобильная Связь":
        await call.message.answer(fmt.text("Введите название вашего мобильного оператора,\n" +
                                           "дату оплаты мобильной связи и время напоминания\n" +
                                           "в формате в формате:\n" +
                                           "Напоминание: Оператор дд чч:мм\n " +
                                           "Например:\nНапоминание: Мегафон 14 15:16"),
                                  parse_mode=aiogram.types.ParseMode.HTML)
    elif choice == "Планер":
        await call.message.answer(fmt.text("Введите название, дату и время события\n" +
                                           "в формате:\n" +
                                           "Напоминание: Событие дд.мм.гггг чч:мм\n" +
                                           "Например:\nНапоминание: Корпоратив 07.08.2021 12:30"),
                                  parse_mode=aiogram.types.ParseMode.HTML)
    elif choice == "Подписки":
        await call.message.answer(fmt.text("Введите название сервиса, на который оформлена подписка,\n" +
                                           "дату оплаты в формате:\n" +
                                           "Напоминание: Сервис дд чч:мм\n" +
                                           "Например:\nНапоминание: Spotify 16 17:18"),
                                  parse_mode=aiogram.types.ParseMode.HTML)
    elif choice == "Приём Лекарств":
        await call.message.answer(fmt.text("Введите название препарата и время приёма\n" +
                                           "Напоминание: Название чч:мм\n" +
                                           "Например:\nНапоминание: Ингавирин 14:15"),
                                  parse_mode=aiogram.types.ParseMode.HTML)
    elif choice == "Удалить":
        await call.message.answer(text="Вы уверены, что хотите удалить все напоминания?",
                                  reply_markup=get_inline_keyboard_from_list(YESNO))


async def reminder_handle_table(message: aiogram.types.Message):
    """
    Добавление напоминания.

    :param message: сообщение боту
    """
    msg = message.text.split()
    print(msg)
    data = dict()
    for i in ("name", "date", "time", "type"):
        data[i] = ''
    if choice in ("День Рождения", "Мобильная Связь", "Планер", "Подписки"):
        data["name"] = ' '.join(msg[1:-2])
        data["date"] = msg[-2]
        data["time"] = msg[-1]
    elif choice == "ЖКХ":
        data["date"] = msg[-2]
        data["time"] = msg[-1]
    elif choice == "Приём Лекарств":
        data["name"] = ' '.join(msg[1:-1])
        data["time"] = msg[-1]
    data["type"] = choice
    database.add_line(data, "reminders")
    await message.answer("Напоминание добавлено", parse_mode=aiogram.types.ParseMode.HTML)


async def yes_no_handle(call: aiogram.types.CallbackQuery):
    """
    Удаление напоминания.

    :param call: сообщение боту
    """
    msg = call.data
    print(msg)
    if msg == "Да":
        database.delete_table_data("reminders")
        await call.message.answer("Все напоминания удалены", parse_mode=aiogram.types.ParseMode.HTML)
    else:
        await call.message.answer("Тогда не будем удалять", parse_mode=aiogram.types.ParseMode.HTML)


def register_handlers(dp: aiogram.Dispatcher) -> None:
    """
    Зарегистрировать обработчики.

    :param dp: диспетчер
    """
    dp.register_message_handler(reminder_handle, regexp=r"^Напоминания")
    dp.register_callback_query_handler(reminder_handle_callback, text=CHOICES)
    dp.register_message_handler(reminder_handle_table, regexp=r"Напоминание: [a-zA-Zа-яА-Я ]*(\d{2}\.\d{2}\.\d{4} |"
                                                              r"\d{2}\.\d{2} |\d{2} )?\d{2}:\d{2}")
    dp.register_callback_query_handler(yes_no_handle, regexp=r"Да|Нет")
