from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from external_services import my_exchange
from keyboards.del_kb import delete_message_button
from lexicon.lexicon import LEXICON
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram import Bot

router: Router = Router()


class FSMLogin(StatesGroup):
    fill_username = State()
    fill_password = State()


@router.message(Command(commands="login"), StateFilter(default_state))
async def process_login_command(message: Message, state: FSMContext):
    await message.delete()
    user_interface_message = \
        await message.answer(text=LEXICON["fill_username"])
    user_interface_message_id = user_interface_message.message_id
    chat_id = user_interface_message.chat.id

    # Опять таки беспочвенный докоп mypy что
    #  Item "None" of "Optional[User]" has no attribute "id"
    if message.from_user is None:
        raise ValueError

    await state.update_data(
        user_interface_message_id=user_interface_message_id,
        chat_id=chat_id,
        user_id=message.from_user.id,
    )
    await state.set_state(FSMLogin.fill_username)


@router.message(StateFilter(FSMLogin.fill_username))
async def process_username_sent(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(username=message.text)
    await message.delete()
    state_data = await state.get_data()
    await bot.edit_message_text(
        text=LEXICON["fill_password"],
        chat_id=state_data["chat_id"],
        message_id=state_data["user_interface_message_id"],
    )
    await state.set_state(FSMLogin.fill_password)


@router.message(StateFilter(FSMLogin.fill_password))
async def process_password_sent_and_login(
    message: Message, bot: Bot, state: FSMContext
):
    await state.update_data(password=message.text)
    await message.delete()
    state_data = await state.get_data()
    await state.clear()
    await state.set_state(default_state)

    if not my_exchange.log_in(state_data):
        await bot.edit_message_text(
            text=LEXICON["wrong_credentials"],
            chat_id=state_data["chat_id"],
            message_id=state_data["user_interface_message_id"],
            reply_markup=delete_message_button(),
        )
        return

    await bot.edit_message_text(
        text=LEXICON["log_in_successfully"],
        chat_id=state_data["chat_id"],
        message_id=state_data["user_interface_message_id"],
        reply_markup=delete_message_button(),
    )
