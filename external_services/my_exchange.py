import json
import requests  # type: ignore
from websocket import create_connection  # type: ignore
from websocket._exceptions import WebSocketBadStatusException  # type: ignore
from aiogram.types import Message
from websockets.legacy.client import connect  # type: ignore
from websockets.legacy.client import WebSocketClientProtocol  # type: ignore
from config_data.config import MyExchange, load_my_exchange_api_config
from database.database import tokens_db
from services.pretty_look import quote_pretty

config: MyExchange = load_my_exchange_api_config()

HOST = config.HOST
GET_QUOTE_URL = config.get_quote
SEND_ORDER_URL = config.send_order
LOGIN_URL = config.login


def is_instrument_supported(instrument: Message | str | None) -> bool:
    if type(instrument) is Message:
        instrument = instrument.text
    get_quote_url = GET_QUOTE_URL.format(HOST=HOST, instrument=instrument)
    try:
        ws = create_connection(get_quote_url)
        ws.close()
    except WebSocketBadStatusException:
        return False
    return True


def quote_connect(instrument):
    get_quote_url = GET_QUOTE_URL.format(HOST=HOST, instrument=instrument)
    quote_endpoint = connect(get_quote_url)
    return quote_endpoint


async def get_quote(quote_endpoint: WebSocketClientProtocol,
                    instrument: str) -> str:
    current_quote_json = await quote_endpoint.recv()
    current_quote = quote_pretty(current_quote_json, instrument)
    return current_quote


def log_in(state_data):
    username = state_data["username"]
    password = state_data["password"]
    response_json = requests.post(
        LOGIN_URL.format(HOST=HOST),
        data={"username": username, "password": password}
    )
    response = json.loads(response_json.text)

    if "auth_token" not in response:
        log_in_status = False

    if "auth_token" in response:
        token = response["auth_token"]
        user_id = state_data["user_id"]
        tokens_db[user_id] = token
        log_in_status = True

    return log_in_status


def send_order(state_data):
    order = dict()
    order["instrument"] = state_data["instrument"]
    order["side_of_deal"] = state_data["side_of_deal"]
    order["price"] = state_data["price"]
    order["amount"] = state_data["amount"]

    instrument = state_data["instrument"]
    token = tokens_db[state_data["user_id"]]
    send_order_url = SEND_ORDER_URL.format(HOST=HOST,
                                           instrument=instrument,
                                           token=token)
    send_order_endpoint = create_connection(send_order_url)

    order_json = json.dumps(order)
    send_order_endpoint.send(order_json)
    send_order_endpoint.close()
