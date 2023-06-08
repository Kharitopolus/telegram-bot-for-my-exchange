from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject
from external_services import my_exchange
from keyboards.del_kb import delete_message_button
from lexicon.lexicon import LEXICON
from aiogram.types import Message
from aiogram import Bot

router: Router = Router()


@router.message(Command(commands="quote"),
                lambda msg: len(msg.text.split()) == 2)
async def view_quote(message: Message, bot: Bot, command: CommandObject):
    await message.delete()

    # or '' - для того, чтобы mypy не говорил что это Optional[str].
    # Проверка, что аргумент у команды есть, выполняется в строке 14.
    instrument = command.args or ""

    if not my_exchange.is_instrument_supported(instrument):
        await message.answer(
            text=LEXICON["instrument_not_supported"],
            reply_markup=delete_message_button(),
        )
        return

    async with my_exchange.quote_connect(instrument) as quote_endpoint:
        current_quote = await my_exchange.get_quote(quote_endpoint, instrument)
        quotation_board = await message.answer(
            text=current_quote, reply_markup=delete_message_button()
        )

        while quotation_board:
            current_quote = \
                await my_exchange.get_quote(quote_endpoint, instrument)
            if quotation_board.text != current_quote:
                try:
                    quotation_board = await bot.edit_message_text(
                        text=current_quote,
                        chat_id=quotation_board.chat.id,
                        message_id=quotation_board.message_id,
                        reply_markup=delete_message_button(),
                    )  # type: ignore
                except TelegramBadRequest:
                    quotation_board = None  # type: ignore


@router.message(Command(commands="quote"))
async def instrument_not_entered(message: Message):
    await message.delete()
    await message.answer(
        text=LEXICON["no_instrument"], reply_markup=delete_message_button()
    )
