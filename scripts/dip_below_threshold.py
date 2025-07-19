import yfinance as yf

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from config.tickers import tickers
from common import common_utils

def check_meta_stock_discount(ticker):
    meta = yf.Ticker(ticker['ticker'])
    hist = meta.history(period="1y")

    # Determine the all-time high price
    all_time_high = hist['Close'].max()

    # Fetch the current stock price
    current_price = hist['Close'].iloc[-1]

    # Calculate the discount percentage
    discount_percentage = ((all_time_high - current_price) / all_time_high) * 100

    if discount_percentage >= ticker['discount_rate']:
        common_utils.notify_message_aleph(
            f"{ticker['ticker']} is trading {discount_percentage:.2f}% below its all-time high.\nAll-time high: ${all_time_high:.2f}\nCurrent price: ${current_price:.2f}\nDiscount: {discount_percentage:.2f}%"
        )
        print(f"{ticker['ticker']} is trading {discount_percentage:.2f}% below its all-time high.\nAll-time high: ${all_time_high:.2f}\nCurrent price: ${current_price:.2f}\nDiscount: {discount_percentage:.2f}%")

def main():
    for ticker in tickers:
        check_meta_stock_discount(ticker)

if __name__ == "__main__":
    main()