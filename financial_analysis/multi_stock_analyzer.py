import pandas as pd
from .stock_analyzer import StockAnalyzer
import concurrent.futures
from .finance_client import FinanceClient
import logging


class MultiStockAnalyzer:
    def __init__(self, tickers: list):
        self.tickers = tickers
        self.client = FinanceClient(tickers)  # Initialize with batch tickers

    def analyze_stock(self, ticker):
        """Analyze a single stock and return the metrics."""
        try:
            # Fetch all data with retry logic
            balance_sheet, financials, cashflow, info = self.client.get_financial_data(
                ticker
            )

            # Log the data for debugging
            logging.debug(
                f"Analyzing {ticker}: balance_sheet size: {balance_sheet.shape}, financials size: {financials.shape}, cashflow size: {cashflow.shape}"
            )

            # Proceed with analysis and handle partial data
            analyzer = StockAnalyzer(ticker, balance_sheet, financials, cashflow, info)
            return analyzer.get_metrics()

        except Exception as e:
            logging.error(f"Error analyzing {ticker}: {e}")
            return {"Ticker": ticker, "Error": str(e)}

    def analyze_stocks(self):
        """Analyze multiple stocks in parallel and return a DataFrame with the specified metrics."""
        results = []

        # Use ThreadPoolExecutor to analyze each stock in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_ticker = {
                executor.submit(self.analyze_stock, ticker): ticker
                for ticker in self.tickers
            }

            # Collect results as they are completed
            for future in concurrent.futures.as_completed(future_to_ticker):
                ticker = future_to_ticker[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logging.error(f"Error analyzing {ticker}: {e}")
                    results.append({"Ticker": ticker, "Error": str(e)})

        # Convert the results list into a DataFrame
        df = pd.DataFrame(results)

        # Round all numeric columns to 4 decimal places
        numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns
        df[numeric_columns] = df[numeric_columns].round(4)

        return df
