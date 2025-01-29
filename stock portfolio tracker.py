import requests

def get_stock_price(symbol):
    """
    Fetch real-time stock price for the given symbol using Alpha Vantage API.
    Replace 'YOUR_ACTUAL_API_KEY' with your Alpha Vantage API key.
    """
    API_URL = "https://www.alphavantage.co/query"
    API_KEY = "YOUR_ACTUAL_API_KEY"

    response = requests.get(API_URL, params={
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": API_KEY
    })

    if response.status_code == 200:
        data = response.json()
        try:
            return float(data["Global Quote"]["05. price"])
        except (KeyError, ValueError):
            print(f"Error parsing data for {symbol}: {data}")
            return None
    else:
        print(f"Error fetching data for {symbol}: {response.status_code}")
        return None

class StockPortfolio:
    def __init__(self):
        self.portfolio = {}

    def add_stock(self, symbol, shares):
        """Add a stock to the portfolio."""
        price = get_stock_price(symbol)
        if price is not None:
            if symbol in self.portfolio:
                self.portfolio[symbol]['shares'] += shares
            else:
                self.portfolio[symbol] = {'shares': shares, 'price': price}
        else:
            print(f"Could not add {symbol} to the portfolio. Price unavailable.")

    def remove_stock(self, symbol, shares):
        """Remove shares of a stock from the portfolio."""
        if symbol in self.portfolio:
            if self.portfolio[symbol]['shares'] > shares:
                self.portfolio[symbol]['shares'] -= shares
            elif self.portfolio[symbol]['shares'] == shares:
                del self.portfolio[symbol]
            else:
                print("You can't remove more shares than you own.")
        else:
            print(f"Stock {symbol} not found in portfolio.")

    def update_prices(self):
        """Update the prices of all stocks in the portfolio."""
        for symbol in self.portfolio:
            price = get_stock_price(symbol)
            if price is not None:
                self.portfolio[symbol]['price'] = price
            else:
                print(f"Could not update price for {symbol}.")

    def view_portfolio(self):
        """Display the portfolio details."""
        total_value = 0
        print("\nPortfolio:")
        print(f"{'Symbol':<10} {'Shares':<10} {'Price':<10} {'Value':<10}")
        print("-" * 40)
        for symbol, details in self.portfolio.items():
            value = details['shares'] * (details['price'] or 0)
            total_value += value
            print(f"{symbol:<10} {details['shares']:<10} {details['price']:<10.2f} {value:<10.2f}")
        print("-" * 40)
        print(f"Total Portfolio Value: {total_value:.2f}\n")

if __name__ == "__main__":
    portfolio = StockPortfolio()

    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. Update Prices")
        print("4. View Portfolio")
        print("5. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares: "))
            portfolio.add_stock(symbol, shares)
        elif choice == "2":
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares to remove: "))
            portfolio.remove_stock(symbol, shares)
        elif choice == "3":
            portfolio.update_prices()
        elif choice == "4":
            portfolio.view_portfolio()
        elif choice == "5":
            print("Exiting tracker. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")
