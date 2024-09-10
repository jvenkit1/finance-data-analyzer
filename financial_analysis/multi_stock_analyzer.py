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
                    # First set of metrics with added Industry
                    metrics = {
                        'Ticker': ticker,
                        'Industry': analyzer.calculator.get_industry(),
                        'DE Ratio': round(analyzer.calculator.calculate_de_ratio() or 0, 4),
                        'ROE': round(analyzer.calculator.calculate_roe() or 0, 4),
                        'Earnings Yield': round(analyzer.calculator.calculate_earnings_yield() or 0, 4),
                        'Dividend Yield': round(analyzer.calculator.calculate_dividend_yield() or 0, 4),
                        'Current Ratio': round(analyzer.calculator.calculate_current_ratio() or 0, 4),
                        'PE to Growth': round(analyzer.calculator.calculate_pe_to_growth() or 0, 4),
                        'Price to Book': round(analyzer.calculator.calculate_price_to_book() or 0, 4),
                        'Current Liabilities': self.format_large_numbers(analyzer.calculator.get_current_liabilities()),
                        'Total Liabilities': self.format_large_numbers(analyzer.calculator.get_total_liabilities()),
                        'Current Assets': self.format_large_numbers(analyzer.calculator.get_current_assets()),
                        'Total Stockholder Equity': self.format_large_numbers(analyzer.calculator.get_total_stockholder_equity()),
                        'Total Shares Outstanding': analyzer.calculator.get_total_shares_outstanding(),
                        'Book Value Per Share': round(analyzer.calculator.calculate_book_value_per_share() or 0, 4),
                        'Price to Sales (P/S)': round(analyzer.calculator.calculate_price_to_sales() or 0, 4),  # P/S ratio
                        'EV/EBITDA': round(analyzer.calculator.calculate_ev_to_ebitda() or 0, 4),  # EV/EBITDA ratio
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
