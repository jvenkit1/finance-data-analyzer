import yfinance as yf
import pandas as pd
import time
import logging


class FinanceClient:
    def __init__(self, tickers: list):
        """
        Initialize FinanceClient to handle multiple tickers.
        Uses yf.Tickers to batch fetch data for all provided tickers.
        """
        self.tickers_obj = yf.Tickers(" ".join(tickers))

    def get_financial_data(self, ticker: str, retries=2, delay=2):
        """
        Fetch financial data for a single stock with retry logic for incomplete data.

        Args:
        ticker (str): The stock ticker symbol.
        retries (int): Number of times to retry if data is incomplete.
        delay (int): Delay between retries in seconds.

        Returns:
        Tuple: balance_sheet, financials, cashflow, info (all are either pd.DataFrame or dict)
        """
        attempt = 0
        while attempt <= retries:
            try:
                stock = self.tickers_obj.tickers[ticker.upper()]

                # Log fetched data types for debugging
                logging.debug(
                    f"Fetched raw data for {ticker}: {type(stock.balance_sheet)}, {type(stock.financials)}, {type(stock.cashflow)}"
                )

                # Fetch financial data
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

                # Check if any data exists and return
                if (
                    not balance_sheet.empty
                    or not financials.empty
                    or not cashflow.empty
                ):
                    return balance_sheet, financials, cashflow, info

                # Log retry attempt
                logging.warning(
                    f"Incomplete data for {ticker}. Retrying... (Attempt {attempt + 1}/{retries})"
                )
                time.sleep(delay)
                attempt += 1

            except Exception as e:
                logging.error(f"Error fetching data for {ticker}: {e}")
                return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), {}

        # If retries failed, log and return empty data
        logging.error(f"Data still incomplete for {ticker} after {retries} retries.")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), info
