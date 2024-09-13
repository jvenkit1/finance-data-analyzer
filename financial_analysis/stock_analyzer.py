from .metrics_calculator import MetricsCalculator


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
        This method returns a dictionary of financial metrics based on the data provided.
        """
        try:
            return {
                "Ticker": self.ticker,
                "Short Name": self.calculator.get_short_name(),
                "Sector": self.calculator.get_sector(),
                "Industry": self.calculator.get_industry(),
                "Revenue": self.calculator.get_revenue(),
                "Operating Income": self.calculator.get_operating_income(),
                "Interest Expense": self.calculator.get_interest_expense(),
                "Book Value of Equity": self.calculator.get_book_value_of_equity(),
                "Total Liabilities": self.calculator.get_total_liabilities(),
                "Effective Tax Rate": self.calculator.calculate_effective_tax_rate(),
                "R&D Expense": self.calculator.get_rnd_expense(),
                "Stock Price": round(self.calculator.get_stock_price() or 0, 4),
                "PE Ratio": round(self.calculator.calculate_pe_ratio() or 0, 4),
                "EPS": round(self.calculator.get_eps() or 0, 4),
                "DE Ratio": round(self.calculator.calculate_de_ratio() or 0, 4),
                "ROE": round(self.calculator.calculate_roe() or 0, 4),
                "Earnings Yield": round(
                    self.calculator.calculate_earnings_yield() or 0, 4
                ),
                "Dividend Yield": round(
                    self.calculator.calculate_dividend_yield() or 0, 4
                ),
                "Current Ratio": round(
                    self.calculator.calculate_current_ratio() or 0, 4
                ),
                "PE to Growth": round(self.calculator.calculate_pe_to_growth() or 0, 4),
                "Price to Book": round(
                    self.calculator.calculate_price_to_book() or 0, 4
                ),
                "Price to Sales (P/S)": round(
                    self.calculator.calculate_price_to_sales() or 0, 4
                ),
                "EV/EBITDA": round(self.calculator.calculate_ev_to_ebitda() or 0, 4),
                "Price to Free Cash Flow": round(
                    self.calculator.calculate_price_to_free_cash_flow() or 0, 4
                ),
                "Total Shares Outstanding": self.calculator.get_total_shares_outstanding(),
                "Book Value Per Share": round(
                    self.calculator.calculate_book_value_per_share() or 0, 4
                ),
                "Payout Ratio": round(self.calculator.calculate_payout_ratio() or 0, 4),
                "Beta (Volatility)": round(self.calculator.get_beta() or 0, 4),
                "Institutional Ownership": round(
                    self.calculator.get_institutional_ownership() or 0, 4
                ),
                "Insider Buying/Selling": round(
                    self.calculator.get_insider_transactions() or 0, 4
                ),
                "Asset Turnover Ratio": round(
                    self.calculator.calculate_asset_turnover_ratio() or 0, 4
                ),
            }
        except Exception as e:
            print(f"Error in calculating metrics for {self.ticker}: {e}")
            return {"Ticker": self.ticker, "Error": str(e)}
