import requests
import json

class StockPortfolio:
    def __init__(self):
        self.portfolio = {}
        self.api_key = "YOUR_ALPHAVANTAGE_API_KEY"  # Replace with your API key
        self.base_url = "https://www.alphavantage.co/query"

    def add_stock(self):
        symbol = input("Enter stock symbol: ").upper()
        shares = int(input("Enter number of shares: "))
        purchase_price = float(input("Enter purchase price per share: "))
        
        if symbol in self.portfolio:
            self.portfolio[symbol]['shares'] += shares
        else:
            self.portfolio[symbol] = {'shares': shares, 'purchase_price': purchase_price}
        print(f"Added {shares} shares of {symbol} at ${purchase_price} per share.")

    def remove_stock(self):
        symbol = input("Enter stock symbol to remove: ").upper()
        shares = int(input("Enter number of shares to remove: "))
        
        if symbol in self.portfolio:
            if shares >= self.portfolio[symbol]['shares']:
                del self.portfolio[symbol]
                print(f"Removed all shares of {symbol}.")
            else:
                self.portfolio[symbol]['shares'] -= shares
                print(f"Removed {shares} shares of {symbol}.")
        else:
            print(f"Stock {symbol} not found in portfolio.")

    def get_stock_price(self, symbol):
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        
        if "Global Quote" in data and data["Global Quote"]:
            if "05. price" in data["Global Quote"]:
                return float(data["Global Quote"]["05. price"])
            else:
                print(f"Stock symbol '{symbol}' found but price data is missing. Response: {data}")
        else:
            print(f"Invalid stock symbol '{symbol}' or data not available. Please check the symbol and try again.")
        return None

    def portfolio_value(self):
        total_value = 0
        for symbol, details in self.portfolio.items():
            current_price = self.get_stock_price(symbol)
            if current_price:
                stock_value = details['shares'] * current_price
                total_value += stock_value
                print(f"{symbol}: {details['shares']} shares @ ${current_price} each = ${stock_value}")
            else:
                print(f"Skipping {symbol} as no valid price data is available.")
        print(f"Total Portfolio Value: ${total_value}")
        return total_value

if __name__ == "__main__":
    portfolio = StockPortfolio()
    while True:
        print("\n1. Add Stock\n2. Remove Stock\n3. View Portfolio Value\n4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            portfolio.add_stock()
        elif choice == "2":
            portfolio.remove_stock()
        elif choice == "3":
            portfolio.portfolio_value()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")
