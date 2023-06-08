from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon import LEXICON


def order_confirm_keyboard() -> InlineKeyboardMarkup:
    confirm = InlineKeyboardButton(
        text=LEXICON["confirm_order"], callback_data="order confirmed"
    )
    cancel = InlineKeyboardButton(
        text=LEXICON["cancel_order"], callback_data="order cancelled"
    )
    keyboard: list[list[InlineKeyboardButton]] = [[confirm, cancel]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def choose_side_of_deal_keyboard() -> InlineKeyboardMarkup:
    ask = InlineKeyboardButton(text=LEXICON["ask"], callback_data="ask")
    bid = InlineKeyboardButton(text=LEXICON["bid"], callback_data="bid")
    keyboard: list[list[InlineKeyboardButton]] = [[ask, bid]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
