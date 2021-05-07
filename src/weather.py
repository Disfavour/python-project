import aiogram
import parsing


weather_obj = parsing.WEATHER()


async def weather_handle(message: aiogram.types.Message):
    """Показать все знаки гороскопа."""
    text = weather_obj.get_data_smart()
    await message.answer(text, parse_mode=aiogram.types.ParseMode.HTML)


def register_handlers(dp: aiogram.Dispatcher) -> None:
    dp.register_message_handler(weather_handle, regexp=r"^Погода$")


if __name__ == "__main__":
    pass
