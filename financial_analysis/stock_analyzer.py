from .finance_client import FinanceClient
from .metrics_calculator import MetricsCalculator
import yfinance as yf

class StockAnalyzer:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.client = FinanceClient(ticker)
        self.balance_sheet, self.financials, self.cashflow, self.info = self.client.get_financial_data()

        # Pass the cashflow data as well to the MetricsCalculator
        self.calculator = MetricsCalculator(self.balance_sheet, self.financials, self.cashflow, self.info)



    def print_metrics(self):
        """Print out the requested metrics for a stock ticker."""
        try:
            print(f"Metrics for {self.ticker}:")
            print(f"Short Name: {self.calculator.get_short_name()}")
            print(f"Sector: {self.calculator.get_sector()}")
            print(f"Industry: {self.calculator.get_industry()}")
            print(f"End Date: {self.calculator.get_end_date()}")
            print(f"Revenue: {self.calculator.get_revenue()}")
            print(f"Operating Income: {self.calculator.get_operating_income()}")
            print(f"Interest Expense: {self.calculator.get_interest_expense()}")
            print(f"Book Value of Equity: {self.calculator.get_book_value_of_equity()}")
            print(f"Book Value of Debt: {self.calculator.get_book_value_of_debt()}")
            print(f"Total Liabilities: {self.calculator.get_total_liabilities()}")
            print(f"Cash: {self.calculator.get_cash()}")
            print(f"Short-Term Investments: {self.calculator.get_short_term_investments()}")
            print(f"Effective Tax Rate: {self.calculator.calculate_effective_tax_rate()}")
            print(f"R&D Expense: {self.calculator.get_rnd_expense()}")
        except Exception as e:
            print(f"Error in calculating metrics for {self.ticker}: {e}")
