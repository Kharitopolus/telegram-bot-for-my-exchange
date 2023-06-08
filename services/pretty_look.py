import json


def quote_pretty(quote: str | bytes, instrument: str) -> str:
    quote_json = json.loads(quote)
    ask = quote_json["ask"]
    bid = quote_json["bid"]
    return f"{instrument}\n\nask: {ask}\n\nbid: {bid}"


def order_pretty(state_data: dict) -> str:
    order = dict()
    order["instrument"] = state_data["instrument"]
    order["side_of_deal"] = state_data["side_of_deal"]
    order["price"] = state_data["price"]
    order["amount"] = state_data["amount"]

    view_pretty = ""
    for key in order:
        view_pretty += f"{key}: {order[key]} \n"
    return view_pretty
