from datetime import datetime

class Stock:
    def __init__(self, symbol, date, open_price, high, low, close):
        self.symbol = symbol
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.open_price = open_price
        self.high = high
        self.low = low
        self.close = close

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "date": self.date.strftime("%Y-%m-%d"),
            "open_price": self.open_price,
            "high": self.high,
            "low": self.low,
            "close": self.close
        }
