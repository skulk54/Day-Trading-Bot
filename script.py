import yfinance as yf
import pandas as pd
import requests
import time
from datetime import datetime

# ✅ Your Discord webhook URLs for each tier
DISCORD_WEBHOOK_URL_TIER_1 = "YOUR WEBHOOK"
DISCORD_WEBHOOK_URL_TIER_2 = "YOUR WEBHOOK"
DISCORD_WEBHOOK_URL_TIER_3 = "YOUR WEBHOOK"
DISCORD_WEBHOOK_URL_TIER_4 = "YOUr WEBHOOK"
DISCORD_WEBHOOK_URL_TIER_5 = "YOUR WEBHOOK"

# ✅ Send a message to Discord
def send_discord_message(message, tier=1):
    # Choose the webhook URL based on the tier
    if tier == 1:
        webhook_url = DISCORD_WEBHOOK_URL_TIER_1
    elif tier == 2:
        webhook_url = DISCORD_WEBHOOK_URL_TIER_2
    elif tier == 3:
        webhook_url = DISCORD_WEBHOOK_URL_TIER_3
    elif tier == 4:
        webhook_url = DISCORD_WEBHOOK_URL_TIER_4
    else:
        webhook_url = DISCORD_WEBHOOK_URL_TIER_5

    try:
        data = {"content": message}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(webhook_url, json=data, headers=headers)

        if response.status_code == 204:
            print(f"✅ Message sent to Tier {tier} Discord.")
        else:
            print(f"❌ Failed to send message to Tier {tier}. Status code: {response.status_code}")
            print(response.text)  # Print the response body for debugging

    except Exception as e:
        print(f"⚠️ Error sending message to Tier {tier} Discord: {e}")

# ✅ RSI Calculation
def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# ✅ Generate Buy/Sell/Hold based on RSI
def generate_signal(rsi_value, ticker, tier):
    if tier >= 3:  # Tier 3 and above
        if rsi_value < 30:
            return f"✅ **BUY** {ticker} — RSI: {rsi_value:.2f}"
        elif rsi_value > 70:
            return f"🛑 **SELL** {ticker} — RSI: {rsi_value:.2f}"
    return f"⏸️ **HOLD** {ticker} — RSI: {rsi_value:.2f}"

# ✅ Main function to track a single stock
def track_stock(ticker, tier=1):
    print(f"🧠 Tracking stock: {ticker}")
    stock_data = yf.download(ticker, period="7d", interval="5m")

    if stock_data.empty:
        print(f"❌ No data found for {ticker}")
        return

    stock_data['RSI'] = calculate_rsi(stock_data)
    latest_rsi = stock_data['RSI'].iloc[-1]
    print(f"📉 Latest RSI for {ticker}: {latest_rsi:.2f}")

    signal = generate_signal(latest_rsi, ticker, tier)
    print(f"📢 Signal: {signal}")
    send_discord_message(signal, tier)

# ✅ Stock Lists for Each Tier
tier_1_tickers = ["AAPL", "TSLA", "PFE", "GOOG", "MSFT"]  # 5 stocks for Bronze (Tier 1)
tier_2_tickers = ["AMZN", "META", "NVDA", "AMD", "BA", "FB", "INTC", "NFLX", "DIS", "PYPL"]  # 10 stocks for Silver (Tier 2)
tier_3_tickers = ["SPY", "QQQ", "IWM", "VTI", "BND", "SPXL", "TSLA", "AAPL", "AMZN", "GOOG", 
                  "MSFT", "META", "NVDA", "AMD", "INTC", "PFE", "NFLX", "BA", "DIS", "PYPL"]  # 20 stocks for Gold (Tier 3)
tier_4_tickers = ["NVDA", "AAPL", "TSLA", "GOOG", "MSFT", "AMZN", "META", "AMD", "PFE", "NFLX", 
                  "SPY", "QQQ", "BND", "VTI", "INTC", "BA", "DIS", "PYPL", "FB", "INTC", "SNAP", 
                  "SPXL", "TQQQ", "SPY", "UVXY", "XLF", "XLY", "XLI", "XLE", "XLB", "XLC", "XBI", "XLV", "VXX", "TLT", "TQQQ"]  # 35 stocks for Platinum (Tier 4)
tier_5_tickers = ["AAPL", "TSLA", "GOOG", "MSFT", "AMZN", "META", "NVDA", "AMD", "BA", "PYPL", 
                  "VTI", "SPY", "BND", "QQQ", "IWM", "SPXL", "SPY", "TQQQ", "VXX", "SPY", "DIS", 
                  "FB", "INTC", "NFLX", "XLF", "XLY", "XLI", "XLE", "XLB", "XLC", "XBI", "XLV", "BABA", "IBM", "COST", "WMT", "CNC"]  # 50+ stocks for Diamond (Tier 5)

# ✅ Run tracker in loop for each tier
def main():
    print("🔍 Scanning Tier 1 stocks... this may take a few seconds.")
    for ticker in tier_1_tickers:
        try:
            track_stock(ticker, tier=1)
        except Exception as e:
            print(f"⚠️ Error tracking {ticker}: {e}")

    print("🔍 Scanning Tier 2 stocks... this may take a few seconds.")
    for ticker in tier_2_tickers:
        try:
            track_stock(ticker, tier=2)
        except Exception as e:
            print(f"⚠️ Error tracking {ticker}: {e}")

    print("🔍 Scanning Tier 3 stocks... this may take a few seconds.")
    for ticker in tier_3_tickers:
        try:
            track_stock(ticker, tier=3)
        except Exception as e:
            print(f"⚠️ Error tracking {ticker}: {e}")

    print("🔍 Scanning Tier 4 stocks... this may take a few seconds.")
    for ticker in tier_4_tickers:
        try:
            track_stock(ticker, tier=4)
        except Exception as e:
            print(f"⚠️ Error tracking {ticker}: {e}")

    print("🔍 Scanning Tier 5 stocks... this may take a few seconds.")
    for ticker in tier_5_tickers:
        try:
            track_stock(ticker, tier=5)
        except Exception as e:
            print(f"⚠️ Error tracking {ticker}: {e}")

# ✅ Start script
if __name__ == "__main__":
    while True:
        main()
        time.sleep(30)  # Check every 30 seconds for Tier 3, 4, and 5
