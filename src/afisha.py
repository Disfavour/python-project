"""Обработка афиши."""
import aiogram
import stuff
import parsing


afisha_obj = parsing.AFISHA()


async def afisha_handle(message: aiogram.types.Message):
    """
    Предоставить выбор вида афиши.

    :param message: сообщение
    """
    options = afisha_obj.options
    afisha_obj.setup()
    await message.answer("Что именно?", reply_markup=stuff.get_inline_keyboard_from_list(options))


async def afisha_handle_callback(call: aiogram.types.CallbackQuery):
    """
    Обработать нажатие кнопки.

    :param call: вызов
    """
    action = call.data
    data = afisha_obj.get_data_smart(action)
    if data:
        await call.message.delete_reply_markup()
        for item in data:
            if item != data[-1]:
                await call.message.answer(item, parse_mode=aiogram.types.ParseMode.HTML)
            else:
                await call.message.answer(
                    item, parse_mode=aiogram.types.ParseMode.HTML, reply_markup=stuff.get_more_inline_keyboard(action))
    else:
        await call.message.delete_reply_markup()
    await call.answer()


def register_handlers(dp: aiogram.Dispatcher) -> None:
    """
    Зарегистрировать обработчики.

    :param dp: диспетчер
    """
    dp.register_message_handler(afisha_handle, regexp=r"^Афиша$")
    dp.register_callback_query_handler(afisha_handle_callback, text=afisha_obj.options)


if __name__ == "__main__":
    pass
