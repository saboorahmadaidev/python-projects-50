import datetime
import time
from plyer import notification
import yfinance as yf


def send_stock_notification(symbol="MSFT"):
    try:
        stock = yf.Ticker(symbol)
        data = stock.info

        if not data:
            print("Failed to fetch stock data.")
            return

        current_price = data.get("currentPrice", "N/A")
        previous_close = data.get("previousClose", "N/A")
        open_price = data.get("open", "N/A")
        day_low = data.get("dayLow", "N/A")
        day_high = data.get("dayHigh", "N/A")
        week_low = data.get("fiftyTwoWeekLow", "N/A")
        week_high = data.get("fiftyTwoWeekHigh", "N/A")
        market_state = data.get("marketState", "N/A")

        market_status = "Open" if market_state == "REGULAR" else "Closed"

        message = (
            f"{symbol} Stock Update\n"
            f"Current Price: {current_price}\n"
            f"Market: {market_status}\n"
            f"Previous Close: {previous_close}\n"
            f"Open: {open_price}\n"
            f"Day Range: {day_low} - {day_high}\n"
            f"52 Week Range: {week_low} - {week_high}\n"
            f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        notification.notify(
            title="📈 Stock Alert",
            message=message,
            timeout=10
        )

        print(message)

    except Exception as e:
        print("Error fetching stock data:", e)



send_stock_notification("MSFT")

time.sleep(5)
