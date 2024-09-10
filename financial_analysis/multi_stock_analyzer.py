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

                # Collect metrics depending on the metric set
                if metric_set == "First":
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
                        'Price to Sales (P/S)': round(analyzer.calculator.calculate_price_to_sales() or 0, 4),
                        'EV/EBITDA': round(analyzer.calculator.calculate_ev_to_ebitda() or 0, 4),
                        'Price to Free Cash Flow': round(analyzer.calculator.calculate_price_to_free_cash_flow() or 0, 4),
                        'Curr Liabilities': self.format_large_numbers(analyzer.calculator.get_current_liabilities()),
                        'Total Liabilities': self.format_large_numbers(analyzer.calculator.get_total_liabilities()),
                        'Curr Assets': self.format_large_numbers(analyzer.calculator.get_current_assets()),
                        'Total Stockholder Equity': self.format_large_numbers(analyzer.calculator.get_total_stockholder_equity()),
                        'Total Shares Outstanding': analyzer.calculator.get_total_shares_outstanding(),
                        'Book Value Per Share': round(analyzer.calculator.calculate_book_value_per_share() or 0, 4),
                        'Payout Ratio': round(analyzer.calculator.calculate_payout_ratio() or 0, 4),
                        'Beta (Volatility)': round(analyzer.calculator.get_beta() or 0, 4),
                        'Institutional Ownership': round(analyzer.calculator.get_institutional_ownership() or 0, 4),
                        'Insider Buying/Selling': round(analyzer.calculator.get_insider_transactions() or 0, 4),
                        'Asset Turnover Ratio': round(analyzer.calculator.calculate_asset_turnover_ratio() or 0, 4),
                        'Free Cash Flow': round(analyzer.calculator.calculate_free_cash_flow() or 0, 4)
                    }
                else:
                    # Default set of metrics
                    metrics = {
                        'Ticker': ticker,
                        'Stock Price': round(analyzer.calculator.get_stock_price() or 0, 4),
                        'PE Ratio': round(analyzer.calculator.calculate_pe_ratio() or 0, 4),
                        'EPS': round(analyzer.calculator.get_eps() or 0, 4),
                        'DE Ratio': round(analyzer.calculator.calculate_de_ratio() or 0, 4),
                        'ROE': round(analyzer.calculator.calculate_roe() or 0, 4),
                        'Earnings Yield': round(analyzer.calculator.calculate_earnings_yield() or 0, 4),
                        'Dividend Yield': round(analyzer.calculator.calculate_dividend_yield() or 0, 4),
                        'Current Ratio': round(analyzer.calculator.calculate_current_ratio() or 0, 4),
                        'PE to Growth': round(analyzer.calculator.calculate_pe_to_growth() or 0, 4),
                        'Price to Book': round(analyzer.calculator.calculate_price_to_book() or 0, 4),
                        'Price to Sales (P/S)': round(analyzer.calculator.calculate_price_to_sales() or 0, 4),
                        'EV/EBITDA': round(analyzer.calculator.calculate_ev_to_ebitda() or 0, 4),
                        'Price to Free Cash Flow': round(analyzer.calculator.calculate_price_to_free_cash_flow() or 0, 4),
                        'Curr Liabilities': self.format_large_numbers(analyzer.calculator.get_current_liabilities()),
                        'Total Liabilities': self.format_large_numbers(analyzer.calculator.get_total_liabilities()),
                        'Curr Assets': self.format_large_numbers(analyzer.calculator.get_current_assets()),
                        'Total Stockholder Equity': self.format_large_numbers(analyzer.calculator.get_total_stockholder_equity()),
                        'Total Shares Outstanding': analyzer.calculator.get_total_shares_outstanding(),
                        'Book Value Per Share': round(analyzer.calculator.calculate_book_value_per_share() or 0, 4),
                        'Payout Ratio': round(analyzer.calculator.calculate_payout_ratio() or 0, 4),
                        'Beta (Volatility)': round(analyzer.calculator.get_beta() or 0, 4),
                        'Institutional Ownership': round(analyzer.calculator.get_institutional_ownership() or 0, 4),
                        'Insider Buying/Selling': round(analyzer.calculator.get_insider_transactions() or 0, 4),
                        'Asset Turnover Ratio': round(analyzer.calculator.calculate_asset_turnover_ratio() or 0, 4)
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
