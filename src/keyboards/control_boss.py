from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def control_boss_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Активировать босса", callback_data="activate_boss")],
        [InlineKeyboardButton(text="Деактивировать босса", callback_data="deactivate_boss")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_menu")]
    ])
    return keyboard