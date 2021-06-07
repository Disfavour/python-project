"""Обработка новостей."""
import aiogram
import os
import gettext

import stuff
import parsing

gettext.install("telbot", os.path.dirname(__file__))


news_obj = parsing.NEWS()
ID_NEWS = "news"


async def news_handle(message: aiogram.types.Message):
    """
    Показать новости.

    :param message: сообщение
    """
    news_obj.make_zero()
    data = news_obj.get_data_smart()
    if data:
        for item in data:
            if item != data[-1]:
                await message.answer(item, parse_mode=aiogram.types.ParseMode.HTML)
            else:
                await message.answer(
                    item, parse_mode=aiogram.types.ParseMode.HTML,
                    reply_markup=stuff.get_more_inline_keyboard(ID_NEWS))
    else:
        raise Exception()


async def news_handle_callback(call: aiogram.types.CallbackQuery):
    """
    Обработать нажатие кнопки.

    :param call: вызов
    """
    data = news_obj.get_data_smart()
    if data:
        await call.message.delete_reply_markup()
        for item in data:
            if item != data[-1]:
                await call.message.answer(item, parse_mode=aiogram.types.ParseMode.HTML)
            else:
                await call.message.answer(
                    item, parse_mode=aiogram.types.ParseMode.HTML,
                    reply_markup=stuff.get_more_inline_keyboard(ID_NEWS))
    else:
        await call.message.delete_reply_markup()
    await call.answer()


def register_handlers(dp: aiogram.Dispatcher) -> None:
    """
    Зарегистрировать обработчики.

    :param dp: диспетчер
    """
    dp.register_message_handler(news_handle, regexp=_(r"^Новости$"))
    dp.register_callback_query_handler(news_handle_callback, text=ID_NEWS)


if __name__ == "__main__":
    pass
