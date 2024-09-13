import pandas as pd
import logging
import yfinance as yf


class FinanceClient:
    def __init__(self, tickers: list):
        # Initialize yf.Tickers for multiple tickers at once
        self.tickers_obj = yf.Tickers(" ".join(tickers))

    def get_financial_data(self, ticker: str):
        """Fetch financial data for a single stock."""
        try:
            stock = self.tickers_obj.tickers[ticker.upper()]
            # Log the fetched raw data to understand the source of the issue
            logging.debug(
                f"Fetched data for {ticker}: stock.balance_sheet: {stock.balance_sheet}, "
                f"stock.financials: {stock.financials}, stock.cashflow: {stock.cashflow}"
            )

            # Safely return empty DataFrames if the data is missing
            balance_sheet = (
                stock.balance_sheet
                if isinstance(stock.balance_sheet, pd.DataFrame)
                else pd.DataFrame()
            )
            financials = (
                stock.financials
                if isinstance(stock.financials, pd.DataFrame)
                else pd.DataFrame()
            )
            cashflow = (
                stock.cashflow
                if isinstance(stock.cashflow, pd.DataFrame)
                else pd.DataFrame()
            )
            info = stock.info or {}

            # Return the data
            return balance_sheet, financials, cashflow, info

        except KeyError as e:
            logging.error(f"Ticker {ticker} not found in batch.")
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), {}
        except Exception as e:
            logging.error(f"Error fetching data for {ticker}: {e}")
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), {}
