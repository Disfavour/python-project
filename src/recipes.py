import aiogram
#import recipes_parsing
import random
import aiogram.utils.markdown as fmt
import database
from stuff import get_inline_keyboard_from_list, get_more_inline_keyboard
from stuff import get_another_inline_keyboard
import re


CHOICE = ["Любой", "По ингредиентам"]
NEXT = "Следующий"
RECIPES_LIST = []
CNT = 0


def form_answer(recipe):
    ingr = ""
    for num, item in enumerate(recipe[1]["ingrs"]):
        ingr += f"{num+1}) {item}\n"
    return fmt.text(
                fmt.text(fmt.hbold(recipe[1]["name"])),
                fmt.text("Ингредиенты:\n", ingr),
                fmt.hlink(recipe[1]["name"], recipe[1]["link"]),
                sep="\n"
            )


async def recipes_handler(message: aiogram.types.Message):
    await message.answer(fmt.text("Нужен рецепт с определенными ингредиентами или любой?"), 
                            reply_markup=get_inline_keyboard_from_list(CHOICE))


async def recipes_handle_callback(call: aiogram.types.CallbackQuery):
    choice = call.data
    if choice == "Любой":
        cur_recipe = database.fetch_by_id(random.randint(1, 4497))[0]
        await call.message.answer(
            form_answer(cur_recipe), 
            parse_mode=aiogram.types.ParseMode.HTML,
            reply_markup=get_more_inline_keyboard(choice))
    elif choice == "По ингредиентам":
        await call.message.answer(fmt.text("Введите ингредиенты с большой буквы через запятую, " + \
                "начиная со слова 'Ингредиенты:'\n Пример: \n" +\
                "'Ингредиенты:  Вишня, Корица, Сахар'\n" + \
                "По возможности уточняйте название ингредиента: " + \
                "вместо 'Перец' введите 'Перец черный' и т.п."),
                                parse_mode=aiogram.types.ParseMode.HTML)


async def recipes_handle_ingreds(message: aiogram.types.Message):
        ingreds = message.text
        ingreds = ingreds.split(":")[1].split(",")
        for k, ingr in enumerate(ingreds):
            while ingr[0].isspace():
                ingr = ingr[1:]
            while ingr[-1].isspace():
                ingr = ingr[:-1]
            ingreds[k] = ingr
        global CNT, RECIPES_LIST
        RECIPES_LIST = database.fetch_by_ingreds(ingreds)
        CNT = 0
        if len(RECIPES_LIST) != 0:
            await message.answer(
                    form_answer(RECIPES_LIST[CNT]), 
                    parse_mode=aiogram.types.ParseMode.HTML,
                    reply_markup=get_another_inline_keyboard(NEXT))
        else:
            await message.answer(fmt.text("Нет рецептов с таким набором ингредиентов"), 
                                parse_mode=aiogram.types.ParseMode.HTML)


async def recipes_handle_ingreds_callback(call: aiogram.types.CallbackQuery):
    global CNT, RECIPES_LIST
    CNT += 1;
    if CNT < len(RECIPES_LIST):
        await call.message.answer(
                    form_answer(RECIPES_LIST[CNT]), 
                    parse_mode=aiogram.types.ParseMode.HTML,
                    reply_markup=get_another_inline_keyboard(call.data))
    else:
        await call.message.answer(fmt.text("Рецепты с такими ингредиентами закончились"), 
                            parse_mode=aiogram.types.ParseMode.HTML)




def register_handlers(dp: aiogram.Dispatcher) -> None:
    dp.register_message_handler(recipes_handler, regexp=r"^Кулинарные рецепты$")
    dp.register_callback_query_handler(recipes_handle_callback, text=CHOICE)
    dp.register_message_handler(recipes_handle_ingreds, regexp=(r"Ингредиенты:(.)*"))
    dp.register_callback_query_handler(recipes_handle_ingreds_callback, text=NEXT)
