import yfinance as yf

class FinanceClient:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
       
    def get_financial_data(self):
        """Fetch financial data for the stock."""
        try:
            balance_sheet = self.stock.balance_sheet
            financials = self.stock.financials
            cashflow = self.stock.cashflow
            info = self.stock.info
            return balance_sheet, financials, cashflow, info
        except Exception as e:
            print(f"Error fetching data for {self.ticker}: {e}")
            return None, None, None, None