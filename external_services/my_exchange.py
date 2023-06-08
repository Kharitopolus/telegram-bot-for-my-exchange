import json
import requests  # type: ignore
from websocket import create_connection  # type: ignore
from websocket._exceptions import WebSocketBadStatusException  # type: ignore
from aiogram.types import Message
from websockets.legacy.client import connect  # type: ignore
from websockets.legacy.client import WebSocketClientProtocol  # type: ignore
from database.database import tokens_db
from services.pretty_look import quote_pretty


def is_instrument_supported(instrument: Message | str | None) -> bool:
    if type(instrument) is Message:
        instrument = instrument.text
    quote_url = f"ws://127.0.0.1:8000/ws/orderbox/{instrument}/"
    try:
        ws = create_connection(quote_url)
        ws.close()
    except WebSocketBadStatusException:
        return False
    return True


def quote_connect(instrument) -> WebSocketClientProtocol:
    quote_url = f"ws://127.0.0.1:8000/ws/orderbox/{instrument}/"
    quote_endpoint = connect(quote_url)
    return quote_endpoint


async def get_quote(quote_endpoint: WebSocketClientProtocol,
                    instrument: str) -> str:
    current_quote_json = await quote_endpoint.recv()
    current_quote = quote_pretty(current_quote_json, instrument)
    return current_quote


def log_in(state_data):
    username = state_data["username"]
    password = state_data["password"]
    login_url = "http://127.0.0.1:8000/token/login/"
    response_json = requests.post(
        login_url, data={"username": username, "password": password}
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
    quote_url = f"ws://127.0.0.1:8000/ws/orderbox/{instrument}/?token={token}"
    quote_endpoint = create_connection(quote_url)

    order_json = json.dumps(order)
    quote_endpoint.send(order_json)
    quote_endpoint.close()
