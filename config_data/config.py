from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class MyExchange:
    HOST: str
    get_quote: str
    send_order: str
    login: str


def load_tg_bot_config(path: str | None = None) -> TgBot:
    env = Env()
    env.read_env(path)
    return TgBot(token=env("BOT_TOKEN"))


def load_my_exchange_api_config(path: str | None = None) -> MyExchange:
    env = Env()
    env.read_env(path)
    return MyExchange(HOST=env("MY_EXCHANGE_HOST"),
                      get_quote=env("GET_QUOTE_URL"),
                      send_order=env("SEND_ORDER_URL"),
                      login=env("LOGIN_URL")
                      )
