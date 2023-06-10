# Telegram bot for my-exchange

-------
Бот выступает интерфейсом для [my-exchange](https://github.com/Kharitopolus/my-exchange). Через него можно смотрет текущие котировки, авторизоваться и выставлять ордера.

![example](./exchange.gif)

## Как запустить

-----
1. Клонировать.
2. Установить зависимости. pip install -r requirements.txt. На windows надо ещё wsl --install, это нужно для работы redis.
3. Сконфигурировать бота.
   1. В .env.example вставить свой токен бота.
   2. Переименовать .env.example в .env
4. Запустить bot.py 
