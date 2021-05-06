import aiogram
from bot import dp
from aiogram.utils.callback_data import CallbackData
import parsing
import aiogram.utils.markdown as fmt


afisha = parsing.AFISHA()
callback_afisha = CallbackData("afisha", "action")
options_afisha = ["Кино", "Театр", "Концерт"]
user_data = {}


@dp.message_handler(regexp=r"^Афиша$")
async def horoscope(message: aiogram.types.Message):
    """Показать все знаки гороскопа."""
    keyboard = aiogram.types.InlineKeyboardMarkup()
    for item in options_afisha:
        keyboard.add(aiogram.types.InlineKeyboardButton(text=item, callback_data=callback_afisha.new(action=item)))

    afisha.cinema_count = 0
    afisha.theatre_count = 0
    afisha.concert_count = 0
    await message.answer("Выбирайте:", reply_markup=keyboard)


@dp.callback_query_handler(callback_afisha.filter(action=[options_afisha[0]]))
async def handle_horoscope_callback(call: aiogram.types.CallbackQuery, callback_data: dict):
    """Кино"""
    keyboard = aiogram.types.InlineKeyboardMarkup()
    keyboard.add(aiogram.types.InlineKeyboardButton(
        text="Ещё", callback_data=callback_afisha.new(action=options_afisha[0])))

    links = afisha.get_links_cinema()
    if links:
        await call.message.delete_reply_markup()
        for link in links:
            if link == links[-1]:
                await call.message.answer(link, reply_markup=keyboard)
            else:
                await call.message.answer(link)
    else:
        call.message.delete_reply_markup()

    await call.answer()


@dp.callback_query_handler(callback_afisha.filter(action=[options_afisha[1]]))
async def handle_horoscope_callback(call: aiogram.types.CallbackQuery, callback_data: dict):
    """Театр"""
    keyboard = aiogram.types.InlineKeyboardMarkup()
    keyboard.add(aiogram.types.InlineKeyboardButton(
        text="Ещё", callback_data=callback_afisha.new(action=options_afisha[1])))

    links = afisha.get_links_theatre()
    if links:
        await call.message.delete_reply_markup()
        for link in links:
            if link == links[-1]:
                await call.message.answer(link, reply_markup=keyboard)
            else:
                await call.message.answer(link)
    else:
        call.message.delete_reply_markup()

    await call.answer()


@dp.callback_query_handler(callback_afisha.filter(action=[options_afisha[2]]))
async def handle_horoscope_callback(call: aiogram.types.CallbackQuery, callback_data: dict):
    """Концерт"""
    keyboard = aiogram.types.InlineKeyboardMarkup()
    keyboard.add(aiogram.types.InlineKeyboardButton(
        text="Ещё", callback_data=callback_afisha.new(action=options_afisha[2])))

    links = afisha.get_links_concert()
    if links:
        await call.message.delete_reply_markup()
        for link in links:
            if link == links[-1]:
                await call.message.answer(f"Спрятал ссылку {fmt.hide_link(link)}", parse_mode=aiogram.types.ParseMode.HTML, reply_markup=keyboard)
            else:
                await call.message.answer(link)
    else:
        call.message.delete_reply_markup()

    await call.answer()


if __name__ == "__main__":
    pass
