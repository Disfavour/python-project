import aiogram
import stuff
import parsing


news_obj = parsing.NEWS()
ID_NEWS = "news"


async def news_handle(message: aiogram.types.Message):
    """Показать новости."""
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
    dp.register_message_handler(news_handle, regexp=r"^Новости$")
    dp.register_callback_query_handler(news_handle_callback, text=ID_NEWS)


if __name__ == "__main__":
    pass
