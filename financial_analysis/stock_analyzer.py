from .finance_client import FinanceClient
from .metrics_calculator import MetricsCalculator
import yfinance as yf

class StockAnalyzer:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)

        # Get the balance sheet, financials, cashflow, and info
        self.balance_sheet = self.stock.balance_sheet
        self.financials = self.stock.financials
        self.cashflow = self.stock.cashflow
        self.info = self.stock.info

        # Fetch historical data (e.g., last 5 years of quarterly data)
        self.history = self.stock.history(period="5y", interval="3mo")  # Quarterly data for 5 years

        # Map historical stock data to relevant metrics (e.g., Revenue, EPS, Free Cash Flow)
        self.history['Revenue'] = self.financials.loc['Total Revenue'].T

        # For EPS, we'll retrieve trailing EPS from the info section (if available)
        self.history['EPS'] = [self.info.get('trailingEps')] * len(self.history)

        # Handle Free Cash Flow (Operating Cash Flow - Capital Expenditure)
        # Use correct labels for Operating Cash Flow and Capital Expenditure
        operating_cash_flow = None
        capex = None

        if 'Operating Cash Flow' in self.cashflow.index:
            operating_cash_flow = self.cashflow.loc['Operating Cash Flow'].T
        elif 'Cash Flow From Continuing Operating Activities' in self.cashflow.index:
            operating_cash_flow = self.cashflow.loc['Cash Flow From Continuing Operating Activities'].T

        if 'Capital Expenditure' in self.cashflow.index:
            capex = self.cashflow.loc['Capital Expenditure'].T
        elif 'Net PPE Purchase And Sale' in self.cashflow.index:
            capex = self.cashflow.loc['Net PPE Purchase And Sale'].T

        # Calculate Free Cash Flow (if both operating cash flow and capex are available)
        if operating_cash_flow is not None and capex is not None:
            self.history['Free Cash Flow'] = operating_cash_flow - capex

        # Initialize the MetricsCalculator with balance_sheet, financials, cashflow, info, and history
        self.calculator = MetricsCalculator(self.balance_sheet, self.financials, self.cashflow, self.info, self.history)

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
