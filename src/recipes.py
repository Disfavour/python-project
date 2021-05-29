import aiogram
#import recipes_parsing
import random
import aiogram.utils.markdown as fmt
import database
from stuff import get_inline_keyboard_from_list, get_more_inline_keyboard
import re


CHOICE = ["Любой", "По ингредиентам"]


def form_answer(recipe):
    ingr = ""
    for num, item in enumerate(recipe[2].split(",")):
        ingr += f"{num+1}) {item}\n"
    return fmt.text(
                fmt.text(fmt.hbold(recipe[1])),
                fmt.text("Ингредиенты:\n", ingr),
                fmt.hlink(recipe[1], recipe[3]),
                sep="\n"
            )


async def recipes_handler(message: aiogram.types.Message):
    await message.answer("Нужен рецепт с определенными ингредиентами или любой?", 
                            reply_markup=get_inline_keyboard_from_list(CHOICE))


async def recipes_handle_callback(call: aiogram.types.CallbackQuery):
    choice = call.data
    if choice == "Любой":
        cur_recipe = database.fetch_by_id(random.randint(1, 3000))[0]
        await call.message.answer(
            form_answer(cur_recipe), 
            parse_mode=aiogram.types.ParseMode.HTML,
            reply_markup=get_more_inline_keyboard(choice))
    elif choice == "По ингредиентам":
        await call.message.answer("Введите ингредиенты через запятую",
                                parse_mode=aiogram.types.ParseMode.HTML)


async def recipes_handle_ingreds(message: aiogram.types.Message):
        ingreds = message.text
        ordered_ingrs = sorted(ingreds.split(":")[1].split(","))
        ingreds = ",".join(ordered_ingrs)
        recipes_lst = database.fetch_by_ingreds(ingreds)
        if len(recipes_lst) != 0:
            for rec in recipes_lst:
                await message.answer(
                    form_answer(rec), 
                    parse_mode=aiogram.types.ParseMode.HTML)
                    #reply_markup=get_more_inline_keyboard(choice))


def register_handlers(dp: aiogram.Dispatcher) -> None:
    dp.register_message_handler(recipes_handler, regexp=r"^Рецепты по ингредиентам$")
    dp.register_callback_query_handler(recipes_handle_callback, text=CHOICE)
    dp.register_message_handler(recipes_handle_ingreds, regexp=(r"Ингредиенты:(.)*"))
