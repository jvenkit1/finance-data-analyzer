from .metrics_calculator import MetricsCalculator
import logging


class StockAnalyzer:
    def __init__(self, ticker: str, balance_sheet, financials, cashflow, info):
        """
        Initialize StockAnalyzer with a ticker and its corresponding financial data.
        Data should already be fetched (e.g., from FinanceClient) and passed in.
        """
        self.ticker = ticker
        # Initialize MetricsCalculator with already fetched data
        self.calculator = MetricsCalculator(balance_sheet, financials, cashflow, info)

    def get_metrics(self):
        """
        Calculate and return the metrics for a stock ticker.
        This method returns a dictionary of financial metrics based on the data provided,
        handling cases where certain metrics may be missing.
        """
        try:
            metrics = {
                "Ticker": self.ticker,
                "Book Value of Equity": (
                    self.calculator.get_book_value_of_equity()
                    if self.calculator.get_book_value_of_equity()
                    else "N/A"
                ),
                "Revenue": (
                    self.calculator.get_revenue()
                    if self.calculator.get_revenue()
                    else "N/A"
                ),
                "Operating Income": (
                    self.calculator.get_operating_income()
                    if self.calculator.get_operating_income()
                    else "N/A"
                ),
                "Interest Expense": (
                    self.calculator.get_interest_expense()
                    if self.calculator.get_interest_expense()
                    else "N/A"
                ),
                "EPS": (
                    self.calculator.get_eps() if self.calculator.get_eps() else "N/A"
                ),
                "PE Ratio": (
                    self.calculator.calculate_pe_ratio()
                    if self.calculator.calculate_pe_ratio()
                    else "N/A"
                ),
                "Total Liabilities": (
                    self.calculator.get_total_liabilities()
                    if self.calculator.get_total_liabilities()
                    else "N/A"
                ),
                "Current Liabilities": (
                    self.calculator.get_current_liabilities()
                    if self.calculator.get_current_liabilities()
                    else "N/A"
                ),
                "Total Assets": (
                    self.calculator._get_balance_sheet_value(["Total Assets"])
                    if self.calculator._get_balance_sheet_value(["Total Assets"])
                    else "N/A"
                ),
                "Current Ratio": (
                    self.calculator.calculate_current_ratio()
                    if self.calculator.calculate_current_ratio()
                    else "N/A"
                ),
                "ROE": (
                    self.calculator.calculate_roe()
                    if self.calculator.calculate_roe()
                    else "N/A"
                ),
                "Earnings Yield": (
                    self.calculator.calculate_earnings_yield()
                    if self.calculator.calculate_earnings_yield()
                    else "N/A"
                ),
                "Dividend Yield": (
                    self.calculator.calculate_dividend_yield()
                    if self.calculator.calculate_dividend_yield()
                    else "N/A"
                ),
                "Price to Free Cash Flow": (
                    self.calculator.calculate_price_to_free_cash_flow()
                    if self.calculator.calculate_price_to_free_cash_flow()
                    else "N/A"
                ),
                "EV/EBITDA": (
                    self.calculator.calculate_ev_to_ebitda()
                    if self.calculator.calculate_ev_to_ebitda()
                    else "N/A"
                ),
                "Price to Book": (
                    self.calculator.calculate_price_to_book()
                    if self.calculator.calculate_price_to_book()
                    else "N/A"
                ),
                "PE to Growth": (
                    self.calculator.calculate_pe_to_growth()
                    if self.calculator.calculate_pe_to_growth()
                    else "N/A"
                ),
                "Total Shares Outstanding": (
                    self.calculator.get_total_shares_outstanding()
                    if self.calculator.get_total_shares_outstanding()
                    else "N/A"
                ),
                "Payout Ratio": (
                    self.calculator.calculate_payout_ratio()
                    if self.calculator.calculate_payout_ratio()
                    else "N/A"
                ),
                "Beta (Volatility)": (
                    self.calculator.get_beta() if self.calculator.get_beta() else "N/A"
                ),
                "Institutional Ownership": (
                    self.calculator.get_institutional_ownership()
                    if self.calculator.get_institutional_ownership()
                    else "N/A"
                ),
                "Insider Transactions": (
                    self.calculator.get_insider_transactions()
                    if self.calculator.get_insider_transactions()
                    else "N/A"
                ),
                "Asset Turnover Ratio": (
                    self.calculator.calculate_asset_turnover_ratio()
                    if self.calculator.calculate_asset_turnover_ratio()
                    else "N/A"
                ),
            }

            # Optional: You can filter out N/A values from the metrics
            filtered_metrics = {k: v for k, v in metrics.items() if v != "N/A"}

            return filtered_metrics

        except Exception as e:
            logging.error(f"Error in calculating metrics for {self.ticker}: {e}")
            return {"Ticker": self.ticker, "Error": str(e)}
