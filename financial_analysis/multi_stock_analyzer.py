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
            # Fetch all data in bulk using the batch `FinanceClient`
            balance_sheet, financials, cashflow, info = self.client.get_financial_data(
                ticker
            )

            # Debugging: Log the types and sizes of the data
            logging.debug(
                f"Analyzing {ticker}: balance_sheet type: {type(balance_sheet)}, financials type: {type(financials)}, cashflow type: {type(cashflow)}, info type: {type(info)}"
            )

            # If balance_sheet, financials, and cashflow are DataFrames, check their emptiness explicitly
            if (
                isinstance(balance_sheet, pd.DataFrame)
                and not balance_sheet.empty
                and isinstance(financials, pd.DataFrame)
                and not financials.empty
                and isinstance(cashflow, pd.DataFrame)
                and info
            ):  # Check if info is a valid dictionary

                # Proceed with the analysis if all data is valid
                analyzer = StockAnalyzer(
                    ticker, balance_sheet, financials, cashflow, info
                )
                return analyzer.get_metrics()

            else:
                # Log the issue with specific data
                logging.error(
                    f"Missing or empty financial data for {ticker}. "
                    f"Balance Sheet Empty: {balance_sheet.empty if isinstance(balance_sheet, pd.DataFrame) else 'Not a DataFrame'}, "
                    f"Financials Empty: {financials.empty if isinstance(financials, pd.DataFrame) else 'Not a DataFrame'}, "
                    f"Cashflow Empty: {cashflow.empty if isinstance(cashflow, pd.DataFrame) else 'Not a DataFrame'}, "
                    f"Info Empty: {'Empty' if not info else 'Present'}"
                )

                return {"Ticker": ticker, "Error": "Missing or empty financial data"}

        except Exception as e:
            logging.error(f"Error analyzing {ticker}: {e}")
            return {"Ticker": ticker, "Error": str(e)}

    def analyze_stocks(self):
        """Analyze multiple stocks in parallel."""
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
                    print(f"Error analyzing {ticker}: {e}")
                    results.append({"Ticker": ticker, "Error": str(e)})

        # Convert the results list into a DataFrame
        df = pd.DataFrame(results)
        return df
