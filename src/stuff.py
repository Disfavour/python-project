"""Полезные данные и функции."""
import aiogram


base_options = ["Гороскоп", "Новости", "Погода", "Афиша",
                "Напоминания", "Счётчик расходов/доходов",
                "Списки покупок", "Кулинарные рецепты", "Валюты"]


def get_inline_keyboard_from_list(items: list) -> aiogram.types.InlineKeyboardMarkup:
    """
    Получить инлайн клавиатуру из листа.

    :param items: список с стрингами, которые станут надписями и колбеком кнопок
    """
    keyboard = aiogram.types.InlineKeyboardMarkup()
    buttons = []
    for item in items:
        buttons.append(aiogram.types.InlineKeyboardButton(text=item, callback_data=item))
    keyboard.add(*buttons)
    return keyboard


def get_more_inline_keyboard(callback_data: str) -> aiogram.types.InlineKeyboardMarkup:
    """
    Получить инлайн клавиатуру с кнопкой "Ещё".

    :param callback_data: колбек для кнопки
    """
    keyboard = aiogram.types.InlineKeyboardMarkup()
    keyboard.add(aiogram.types.InlineKeyboardButton(text="Ещё", callback_data=callback_data))
    return keyboard


def get_another_inline_keyboard(callback_data: str) -> aiogram.types.InlineKeyboardMarkup:
    """
    Получить инлайн клавиатуру с кнопкой "Следующий".

    :param callback_data: колбек для кнопки
    """
    keyboard = aiogram.types.InlineKeyboardMarkup()
    keyboard.add(aiogram.types.InlineKeyboardButton(text="Следующий", callback_data=callback_data))
    return keyboard


if __name__ == "__main__":
    pass
