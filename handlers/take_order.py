from aiogram import Router, F
from aiogram.filters import Command, Text
from database.database import tokens_db
from keyboards.del_kb import delete_message_button
from keyboards.take_order import order_confirm_keyboard, \
    choose_side_of_deal_keyboard
from lexicon.lexicon import LEXICON
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from aiogram import Bot
from external_services import my_exchange
from services.pretty_look import order_pretty

router: Router = Router()


class FSMTakeOrder(StatesGroup):
    fill_instrument = State()
    fill_side_of_deal = State()
    fill_price = State()
    fill_amount = State()
    confirm_order = State()


@router.message(
    Command(commands="make_order"),
    lambda message: message.from_user.id in tokens_db
)
async def start_take_order_form(message: Message, state: FSMContext):
    await message.delete()

    await state.set_state(FSMTakeOrder.fill_instrument)
    user_interface_message = \
        await message.answer(text=LEXICON["fill_instrument"])
    if message.from_user is None:
        raise ValueError
    await state.update_data(
        user_id=message.from_user.id,
        user_interface_message_id=user_interface_message.message_id,
        chat_id=user_interface_message.chat.id,
    )


@router.message(Command(commands="make_order"))
async def user_dont_login(message: Message, state: FSMContext):
    await message.delete()
    await message.answer(
        text=LEXICON["user_dont_login"], reply_markup=delete_message_button()
    )
    await state.set_state(default_state)


@router.message(
    my_exchange.is_instrument_supported,
    StateFilter(FSMTakeOrder.fill_instrument)
)
async def fill_instrument(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(instrument=message.text)
    await message.delete()

    await state.set_state(FSMTakeOrder.fill_side_of_deal)
    state_data = await state.get_data()
    await bot.edit_message_text(
        text=LEXICON["fill_side_of_deal"],
        chat_id=state_data["chat_id"],
        message_id=state_data["user_interface_message_id"],
        reply_markup=choose_side_of_deal_keyboard(),
    )


@router.message(StateFilter(FSMTakeOrder.fill_instrument))
async def instrument_not_supported(message: Message,
                                   bot: Bot,
                                   state: FSMContext):
    await message.delete()

    state_data = await state.get_data()
    await bot.edit_message_text(
        text=LEXICON["instrument_not_supported"],
        chat_id=state_data["chat_id"],
        message_id=state_data["user_interface_message_id"],
        reply_markup=delete_message_button(),
    )
    await state.set_state(default_state)


@router.callback_query(
    StateFilter(FSMTakeOrder.fill_side_of_deal), Text(text=["ask", "bid"])
)
async def fill_side_of_deal(callback: CallbackQuery, state: FSMContext):
    await state.update_data(side_of_deal=callback.data)

    await state.set_state(FSMTakeOrder.fill_price)
    if not callback.message:
        raise ValueError
    await callback.message.edit_text(text=LEXICON["fill_price"])


@router.message(StateFilter(FSMTakeOrder.fill_price), F.text.isdigit())
async def fill_price(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(price=message.text)
    await message.delete()

    await state.set_state(FSMTakeOrder.fill_amount)
    state_data = await state.get_data()
    await bot.edit_message_text(
        text=LEXICON["fill_amount"],
        chat_id=state_data["chat_id"],
        message_id=state_data["user_interface_message_id"],
    )


@router.message(StateFilter(FSMTakeOrder.fill_price))
async def invalid_price(message: Message, bot: Bot, state: FSMContext):
    await message.delete()
    state_data = await state.get_data()
    await bot.edit_message_text(
        text=LEXICON["invalid_price"],
        chat_id=state_data["chat_id"],
        message_id=state_data["user_interface_message_id"],
    )
    await state.set_state(FSMTakeOrder.fill_price)


@router.message(StateFilter(FSMTakeOrder.fill_amount), F.text.isdigit())
async def fill_amount(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(amount=message.text)
    await message.delete()

    await state.set_state(FSMTakeOrder.confirm_order)
    state_data = await state.get_data()
    await bot.edit_message_text(
        text=LEXICON["confirm_order_?"] + "\n\n" + order_pretty(state_data),
        chat_id=state_data["chat_id"],
        message_id=state_data["user_interface_message_id"],
        reply_markup=order_confirm_keyboard(),
    )


@router.message(StateFilter(FSMTakeOrder.fill_amount))
async def invalid_amount(message: Message, bot: Bot, state: FSMContext):
    await message.delete()
    state_data = await state.get_data()
    await bot.edit_message_text(
        text=LEXICON["invalid_amount"],
        chat_id=state_data["chat_id"],
        message_id=state_data["user_interface_message_id"],
    )
    await state.set_state(FSMTakeOrder.fill_amount)


@router.callback_query(StateFilter(FSMTakeOrder.confirm_order))
async def send_order(callback: CallbackQuery, state: FSMContext):
    if not callback.data or not callback.message:
        raise ValueError

    if callback.data == "order canceled":
        await callback.message.answer(
            text=LEXICON["order_canceled"],
            reply_markup=delete_message_button()
        )

    if callback.data == "order confirmed":
        state_data = await state.get_data()
        my_exchange.send_order(state_data)
        await callback.message.answer(
            text=LEXICON["order_accepted"],
            reply_markup=delete_message_button()
        )
    await callback.message.delete()
