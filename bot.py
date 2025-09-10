import yfinance as yf 
import pandas as pd
from aiogram import Bot, Dispatcher, executor, types
import random

# === SETTINGS ===
TOKEN = "7644871200:AAF3oKcMkS8qLMjH_31d-AYRQUQ3aglqhMs"  # insert your token from BotFather
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# === FUNCTION TO CALCULATE SIGNAL ===
def get_signal(pair="EURUSD"):
    # If it's forex (letters only, like EURUSD), add =X
    if pair.isalpha():
        ticker = pair + "=X"
    else:
        ticker = pair

    data = yf.download(ticker, period="1mo", interval="1h")

    if data.empty:
        return f"⚠️ No data for {pair}"

    # Moving Averages
    data["SMA50"] = data["Close"].rolling(window=50).mean()
    data["SMA200"] = data["Close"].rolling(window=200).mean()

    # Last values
    sma50 = float(data["SMA50"].iloc[-1])
    sma200 = float(data["SMA200"].iloc[-1])
    last_close = float(data["Close"].iloc[-1])

    # Check for NaN
    if pd.isna(sma50) or pd.isna(sma200):
        return f"⚠️ Not enough data for {pair}"

    # Signal generation
    if sma50 > sma200:
        signal = "📈 BUY"
    elif sma50 < sma200:
        signal = "📉 SELL"
    else:
        signal = "⏸ HOLD"

    # Random time from 1 to 5 minutes
    trade_time = random.randint(1, 5)

    return (
        f"📊 Pair: {pair}\n"
        f"Signal: {signal}\n"
        f"Price: {round(last_close, 5)}\n"
        f"⏱ Time: {trade_time} min"
    )

# === BOT COMMANDS ===
@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.reply(
        "Hello! 🚀\n"
        "Use the command in the format:\n"
        "`/signal EURUSD`\n\n"
        "Examples of tickers:\n"
        "Forex: EURUSD, GBPJPY, USDJPY, GBPUSD\n"
        "Crypto: BTC-USD, ETH-USD",
        parse_mode="Markdown"
    )

@dp.message_handler(commands=["signal"])
async def signal(msg: types.Message):
    args = msg.get_args()
    pair = args if args else "EURUSD"
    try:
        result = get_signal(pair.upper())
        await msg.reply(result)
    except Exception as e:
        await msg.reply(f"Error: {e}")

# === RUN BOT ===
if __name__ == "__main__":
    executor.start_polling(dp)
