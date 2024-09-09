import pandas as pd
from .stock_analyzer import StockAnalyzer

class MultiStockAnalyzer:
    def __init__(self, tickers: list):
        self.tickers = tickers

    def format_large_numbers(self, value):
        """Helper function to format numbers in billions ('B') or millions ('M')."""
        if isinstance(value, (int, float)):
            if abs(value) >= 1_000_000_000:  # Billions
                return f"{value / 1_000_000_000:.4f}B"
            elif abs(value) >= 1_000_000:  # Millions
                return f"{value / 1_000_000:.4f}M"
        return value

    def analyze_stocks(self, metric_set="Default"):
        """Analyze multiple stocks and return a DataFrame with the specified metrics."""
        results = []

        # Loop through each ticker and collect the metrics
        for ticker in self.tickers:
            try:
                analyzer = StockAnalyzer(ticker)

                if metric_set == "First":
                    # First set of metrics with the new ones added
                    metrics = {
                        'Ticker': ticker,
                        'Industry': analyzer.calculator.get_industry(),
                        'Revenue Growth (YoY)': round(analyzer.calculator.calculate_revenue_growth('yoy') or 0, 4),
                        'Revenue Growth (QoQ)': round(analyzer.calculator.calculate_revenue_growth('qoq') or 0, 4),
                        'EPS Growth (YoY)': round(analyzer.calculator.calculate_eps_growth('yoy') or 0, 4),
                        'EPS Growth (QoQ)': round(analyzer.calculator.calculate_eps_growth('qoq') or 0, 4),
                        'FCF Growth (YoY)': round(analyzer.calculator.calculate_fcf_growth('yoy') or 0, 4),
                        'FCF Growth (QoQ)': round(analyzer.calculator.calculate_fcf_growth('qoq') or 0, 4),
                        'Gross Profit Margin': round(analyzer.calculator.calculate_gross_profit_margin() or 0, 4),
                        'Operating Profit Margin': round(analyzer.calculator.calculate_operating_profit_margin() or 0, 4),
                        'Net Profit Margin': round(analyzer.calculator.calculate_net_profit_margin() or 0, 4),
                        'Return on Invested Capital (ROIC)': round(analyzer.calculator.calculate_roic() or 0, 4),
                        'Debt-to-Equity (D/E) Ratio': round(analyzer.calculator.calculate_de_ratio() or 0, 4),
                        'Current Ratio': round(analyzer.calculator.calculate_current_ratio() or 0, 4),
                        'Quick Ratio': round(analyzer.calculator.calculate_quick_ratio() or 0, 4),
                        'Price-to-Free Cash Flow (P/FCF)': round(analyzer.calculator.calculate_pfcf() or 0, 4),
                        'PEG Ratio': round(analyzer.calculator.calculate_peg_ratio() or 0, 4),
                        'Dividend Yield': round(analyzer.calculator.calculate_dividend_yield() or 0, 4),
                        'Payout Ratio': round(analyzer.calculator.calculate_payout_ratio() or 0, 4),
                        'Beta (Volatility)': round(analyzer.calculator.get_beta() or 0, 4),
                        'Institutional Ownership': round(analyzer.calculator.get_institutional_ownership() or 0, 4),
                        'Insider Buying/Selling': round(analyzer.calculator.get_insider_transactions() or 0, 4),
                        'Asset Turnover Ratio': round(analyzer.calculator.calculate_asset_turnover_ratio() or 0, 4),
                    }
                else:
                    # Default set of metrics (previously implemented)
                    metrics = {
                        'Ticker': ticker,
                        'Short Name': analyzer.calculator.get_short_name(),
                        'Sector': analyzer.calculator.get_sector(),
                        'Industry': analyzer.calculator.get_industry(),
                        'End Date': analyzer.calculator.get_end_date(),
                        'Revenue': self.format_large_numbers(analyzer.calculator.get_revenue()),
                        'Operating Income': self.format_large_numbers(analyzer.calculator.get_operating_income()),
                        'Interest Expense': self.format_large_numbers(analyzer.calculator.get_interest_expense()),
                        'Book Value of Equity': self.format_large_numbers(analyzer.calculator.get_book_value_of_equity()),
                        'Book Value of Debt': self.format_large_numbers(analyzer.calculator.get_book_value_of_debt()),
                        'Total Liabilities': self.format_large_numbers(analyzer.calculator.get_total_liabilities()),
                        'Cash': self.format_large_numbers(analyzer.calculator.get_cash()),
                        'Short-Term Investments': self.format_large_numbers(analyzer.calculator.get_short_term_investments()),
                        'Effective Tax Rate': round(analyzer.calculator.calculate_effective_tax_rate() or 0, 4),
                        'R&D Expense': self.format_large_numbers(analyzer.calculator.get_rnd_expense())
                    }

                # Add metrics to the results list
                results.append(metrics)

            except Exception as e:
                print(f"Error analyzing {ticker}: {e}")
                results.append({'Ticker': ticker, 'Error': str(e)})

        # Convert the results list into a DataFrame
        df = pd.DataFrame(results)

        # Round all numeric columns to 4 decimal places
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        df[numeric_columns] = df[numeric_columns].round(4)

        return df
