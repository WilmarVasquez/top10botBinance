import asyncio
from telebot.async_telebot import AsyncTeleBot
import binance
import requests
import os

bot = AsyncTeleBot(token='TELEGRAM_BOT_TOKEN')
client = binance.Client()

def get_top_coins():
    response = requests.get('https://api.binance.com/api/v3/ticker/24hr')
    data = response.json()
    volumes = [(coin['symbol'], float(coin['volume']), float(coin['lastPrice']), coin['symbol'][-4:]=="USDT") for coin in data]
    volumes_sorted = sorted(volumes, key=lambda x: x[1]*x[2], reverse=True)
    top_coins = [coin for coin in volumes_sorted if coin[0].endswith('USDT')][:10]
    return top_coins

async def update_listener(messages):
    for message in messages:
        if message.text == '/top':
            top_coins = get_top_coins()
            text = "Top 10 monedas con mayor volumen de negociación en las últimas 24 horas:\n"
            for i, coin in enumerate(top_coins):
                text += f"{i+1}. {coin[0]} ({coin[2]} USDT)\n"
            await bot.send_message(message.chat.id, text)

bot.set_update_listener(update_listener)

async def main():
    while True:
        try:
            await bot.polling(timeout=30)
        except Exception as e:
            print(e)
            # agregar un retraso para evitar un bucle infinito de errores
            await asyncio.sleep(10)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
	
