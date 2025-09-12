import logging
import random
import asyncio
import yfinance as yf
import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# ==== ВСТАВЬ СВОЙ ТОКЕН СЮДА ====
API_TOKEN = "YOUR_BOT_TOKEN"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Получение случайного сигнала
def get_signal():
    pairs = ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", "USDCAD=X"]
    pair = random.choice(pairs)
    
    data = yf.download(pair, period="1d", interval="1m")
    if data.empty:
        return None
    
    last_price = round(data["Close"].iloc[-1], 5)
    signal_type = random.choice(["📈 BUY", "📉 SELL"])
    time_to_exit = random.randint(1, 5)  # минуты
    
    return {
        "pair": pair.replace("=X", ""),
        "signal": signal_type,
        "price": last_price,
        "time": time_to_exit
    }

# Команда /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("👋 Привет! Отправь /signal, чтобы получить торговый сигнал.")

# Команда /signal
@dp.message(Command("signal"))
async def signal_handler(message: types.Message):
    signal = get_signal()
    if signal:
        response = (
            f"📊 Pair: {signal['pair']}\n"
            f"Signal: {signal['signal']}\n"
            f"Price: {signal['price']}\n"
            f"⏱ Time: {signal['time']} min"
        )
        await message.answer(response)
    else:
        await message.answer("❌ Не удалось получить данные. Попробуй ещё раз.")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
