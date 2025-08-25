# scripts/csp_reminder.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import yfinance as yf
from config.tickers import tickers
from common import common_utils
from datetime import datetime, timedelta

def check_price_drop(ticker, days=5, threshold=-0.10):
    """
    Check if a stock's price has dropped more than the threshold (e.g., 10%) over the last N days.
    Returns True if the drop exceeds the threshold, False otherwise.
    """
    try:
        stock = yf.Ticker(ticker)
        # Fetch historical data for the last N+1 days to compare
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days + 1)
        history = stock.history(start=start_date, end=end_date, interval="1d")
        
        if len(history) < 2:
            print(f"Insufficient data for {ticker}")
            return False
        
        # Get the closing prices for the earliest and latest available days
        first_close = history['Close'].iloc[0]
        last_close = history['Close'].iloc[-1]
        print(f"{ticker}: {first_close} ---- {last_close}")
        
        # Calculate percentage change
        percent_change = (last_close - first_close) / first_close
        return percent_change <= threshold
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return False

def main():
    for item in tickers:
        ticker = item['ticker']
        # Use csp_percentage_down if provided, else default to -0.10
        threshold = item.get('csp_percentage_down', -0.15)
        if check_price_drop(ticker, threshold=threshold):
            print(f"Reminder to do cash-secured puts on {ticker}")
            common_utils.notify_message_aleph(f"Reminder to do cash-secured puts on {ticker}")

if __name__ == "__main__":
    main()