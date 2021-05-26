import aiogram
import recipes_parsing
import aiogram.utils.markdown as fmt


def form_answer(recipe):
    ingr = ""
    for num, item in enumerate(recipe["Ингредиенты"]):
        ingr += f"{num+1}) {item},\n"
    return fmt.text(
                fmt.text(fmt.hbold(recipe["Название блюда"])),
                fmt.text("Ингредиенты:\n", ingr),
                fmt.hlink(recipe["Название блюда"], recipe["Ссылка на рецепт"]),
                sep="\n"
            )


async def recipes_handler(message: aiogram.types.Message):
    res = recipes_parsing.parse()
    cur = res[0]
    await message.answer(
            form_answer(cur), 
            parse_mode=aiogram.types.ParseMode.HTML)


def register_handlers(dp: aiogram.Dispatcher) -> None:
    dp.register_message_handler(recipes_handler, regexp=r"^Рецепты по ингредиентам$")
