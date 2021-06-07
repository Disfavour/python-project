"""Обработка напоминаний."""
import asyncio

import aiocron
import aiogram
import aiogram.utils.markdown as fmt
import nest_asyncio

from . import database
from .stuff import get_inline_keyboard_from_list

CHOICES = ["День Рождения", "ЖКХ", "Мобильная Связь", "Планер", "Подписки", "Приём Лекарств", "Удалить"]
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
    async def at_time():
        try:
            for j in CHOICES[:-1]:
                res = database.get_line_notif(j)
                print(res)
                for i in res:
                    if i is not None:
                        notif = 'Напоминяние: {} – {} {}'.format(i[-1], i[-2], i[1])
                        await message.answer(notif, parse_mode=aiogram.types.ParseMode.HTML)
        except Exception as error:
            print(error)

    asyncio.get_event_loop().run_forever()


async def reminder_handle_callback(call: aiogram.types.CallbackQuery):
    """
    Обработка нажатия на кнопки встроенной клавиатуры.

    :param call: вызов бота
    """
    global choice
    choice = call.data
    if choice == "День Рождения":
        await call.message.answer(fmt.text("Введите ФИО и день рождения именинника в формате:\n" +
                                           "Напоминание: Фамилия Имя Отчество дд.мм.гггг\n" +
                                           "Например:\nНапоминание: Иванов Иван Иванович 11.12.1999"),
                                  parse_mode=aiogram.types.ParseMode.HTML)
    elif choice == "ЖКХ":
        await call.message.answer(fmt.text("Введите дату оплаты ЖКХ в формате:\n" +
                                           "Напоминание: дд\n" +
                                           "Например:\nНапоминание: 17"),
                                  parse_mode=aiogram.types.ParseMode.HTML)
    elif choice == "Мобильная Связь":
        await call.message.answer(fmt.text("Введите название вашего мобильного оператора" +
                                           " и дату оплаты мобильной связи в формате:\n" +
                                           "Напоминание: Оператор дд\n " +
                                           "Например:\nНапоминание: Мегафон 14"),
                                  parse_mode=aiogram.types.ParseMode.HTML)
    elif choice == "Планер":
        await call.message.answer(fmt.text("Введите название и дату события (опционально можно написать время)\n" +
                                           "в формате:\n" +
                                           "Напоминание: Событие дд.мм.гггг чч:мм\nили\n" +
                                           "Или\n Событие дд.мм.гггг\n" +
                                           "Например:\nНапоминание: Корпоратив 07.08.2021 12:30"),
                                  parse_mode=aiogram.types.ParseMode.HTML)
    elif choice == "Подписки":
        await call.message.answer(fmt.text("Введите название сервиса, на который оформлена подписка,\n" +
                                           "и дату оплаты в формате:\n" +
                                           "Напоминание: Сервис дд\n" +
                                           "Например:\nНапоминание:  Spotify 16"),
                                  parse_mode=aiogram.types.ParseMode.HTML)
    elif choice == "Приём Лекарств":
        await call.message.answer(fmt.text("Введите название препарата и время приёма\n" +
                                           "Напоминание: Название чч:мм\n" +
                                           "Например:\nНапоминание: Ингавирин 14:15"),
                                  parse_mode=aiogram.types.ParseMode.HTML)
    elif choice == "Удалить":
        await call.message.answer(fmt.text("Выберите категорию, из которой нужно удалить напоминание"),
                                  reply_markup=get_inline_keyboard_from_list(CHOICES[:-1]))


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
    if choice in ("День Рождения", "Мобильная Связь", "Подписки"):
        data["name"] = ' '.join(msg[1:-1])
        data["date"] = msg[-1]
    elif choice == "ЖКХ":
        data["date"] = msg[-1]
    elif choice == "Планер":
        data["name"] = ' '.join(msg[1:-2])
        data["date"] = msg[-2]
        data["time"] = msg[-1]
    elif choice == "Приём Лекарств":
        data["name"] = ' '.join(msg[1:-1])
        data["time"] = msg[-1]
    data["type"] = choice
    database.add_line(data, "reminders")
    await message.answer("Напоминание добавлено", parse_mode=aiogram.types.ParseMode.HTML)


def register_handlers(dp: aiogram.Dispatcher) -> None:
    """
    Зарегистрировать обработчики.

    :param dp: диспетчер
    """
    dp.register_message_handler(reminder_handle, regexp=r"^Напоминания")
    dp.register_callback_query_handler(reminder_handle_callback, text=CHOICES)
    dp.register_message_handler(reminder_handle_table, regexp=r"Напоминание: ([a-zA-Zа-яА-Я ]+ ((\d{2}\.\d{2}"
                                                              r"(\.\d{2,4})?( \d{2}:\d{2})?|"
                                                              r"(\d{2}(:\d{2})?)))|\d+|[а-яА-Я]+)")
