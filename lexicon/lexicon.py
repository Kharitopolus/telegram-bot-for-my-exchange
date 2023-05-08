LEXICON: dict[str, str] = {
    "start": 'Это бот биржи. Все команды можно посмотреть в "Меню"',
    "no_instrument": 'Надо указать инструмент. Например: "/quote HP"',
    "instrument_not_supported":
        "Такого инструмента нет в списке поддерживаемых.",
    "fill_username":
        "Чтобы прервать заполнение формы введите /cancel."
        " \n\nВведите имя пользователя",
    "fill_password": "Введите пароль",
    "wrong_credentials":
        "Неверное имя пользователя или пароль."
        " \n\nПопробовать снова: /login",
    "logged_in": "Вы авторизировались",
    "fill_instrument":
        "Чтобы прервать заполнение формы введите /cancel."
        " \n\nВыберите инструмент",
    "dont_login":
        "Выставлять ордера можно только если выполнен вход в аккаунт: /login",
    "fill_side_of_deal": "Выберите сторону сделки",
    "fill_price": "Укажите цену",
    "invalid_price": "Цена должна быть цифрой. \nПовторите попытку",
    "fill_amount": "Укажите количество",
    "invalid_amount": "Количество должно быть цифрой. \nПовторите попытку",
    "confirm": "Вы подтверждайте выставление ордера:",
    "order_accepted": "Ордер принят",
    "order_canceled": "Ордер отменён",
    "del": "❎",
    "yes": "да",
    "no": "нет",
    "ask": "ask",
    "bid": "bid",
    "cancel": "Вы прервали заполнение формы",
    "unforeseen_action": 'Все доступные команды можно посмотреть в "Меню"',
}

LEXICON_COMMANDS: dict[str, str] = {
    "/login": "Вход в аккаунт",
    "/quote":
        "<<имя инструмента>>(обязательно). Показывает котировки.",
    "/make_order":
        "Выставить ордер. (Доступно только авторизированным пользователям)",
}
