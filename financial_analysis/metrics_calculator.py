import pandas as pd


class MetricsCalculator:
    def __init__(
        self,
        balance_sheet: pd.DataFrame,
        financials: pd.DataFrame,
        cashflow: pd.DataFrame,
        info: dict,
    ):
        """
        Initialize the MetricsCalculator with balance sheet, financials, cashflow, and info.
        These data sources are assumed to be pre-fetched and passed into the constructor.
        """
        self.balance_sheet = balance_sheet
        self.financials = financials
        self.cashflow = cashflow
        self.info = info

        # Cache values to avoid repeated calculations
        self._cached_values = {}

    def _get_balance_sheet_value(self, keys):
        """
        Helper method to retrieve balance sheet values using multiple possible keys.
        """
        for key in keys:
            if key in self.balance_sheet.index:
                if not self.balance_sheet.loc[key].empty:
                    return self.balance_sheet.loc[key].iloc[0]
        return None

    def _get_financials_value(self, keys):
        """
        Helper method to retrieve financial values using multiple possible keys.
        """
        for key in keys:
            if key in self.financials.index:
                if not self.financials.loc[key].empty:
                    return self.financials.loc[key].iloc[0]
        return None

    def _get_cashflow_value(self, keys):
        """
        Helper method to retrieve cash flow values using multiple possible keys.
        """
        for key in keys:
            if key in self.cashflow.index:
                if not self.cashflow.loc[key].empty:
                    return self.cashflow.loc[key].iloc[0]
        return None

    def get_industry(self):
        """Retrieve the industry from the info dictionary."""
        return self.info.get("industry", None)

    def get_sector(self):
        """Retrieve the sector from the info dictionary."""
        return self.info.get("sector", None)

    def get_short_name(self):
        """Retrieve the short name from the info dictionary."""
        return self.info.get("shortName", None)

    def get_stock_price(self):
        """Retrieve the current stock price from the info dictionary."""
        return self.info.get("currentPrice", None)

    def calculate_pe_ratio(self):
        """Calculate the Price-to-Earnings (PE) ratio from the info dictionary."""
        return self.info.get("trailingPE", None)

    def get_eps(self):
        """Retrieve the Earnings per Share (EPS) from the info dictionary."""
        return self.info.get("trailingEps", None)

    def calculate_de_ratio(self):
        """Calculate the Debt-to-Equity (DE) ratio using Total Liabilities and Common Stock Equity."""
        total_liabilities = self._get_balance_sheet_value(
            ["Total Liabilities Net Minority Interest", "Total Liabilities"]
        )
        total_stockholder_equity = self._get_balance_sheet_value(
            ["Common Stock Equity", "Stockholders Equity"]
        )
        if total_liabilities is None or total_stockholder_equity is None:
            return None
        return total_liabilities / total_stockholder_equity

    def calculate_roe(self):
        """Calculate the Return on Equity (ROE) using Net Income and Stockholder Equity."""
        net_income = self._get_financials_value(["Net Income"])
        total_stockholder_equity = self._get_balance_sheet_value(
            ["Common Stock Equity", "Stockholders Equity"]
        )
        if net_income is None or total_stockholder_equity is None:
            return None
        return net_income / total_stockholder_equity

    def calculate_earnings_yield(self):
        """Calculate the Earnings Yield using Net Income and Market Cap."""
        net_income = self._get_financials_value(["Net Income"])
        market_cap = self.info.get("marketCap", None)
        if net_income is None or market_cap is None:
            return None
        return net_income / market_cap

    def calculate_dividend_yield(self):
        """Calculate the Dividend Yield from the info dictionary."""
        return self.info.get("dividendYield", None)

    def calculate_current_ratio(self):
        """Calculate the Current Ratio using Total Current Assets and Total Current Liabilities."""
        current_assets = self._get_balance_sheet_value(["Current Assets"])
        current_liabilities = self._get_balance_sheet_value(["Current Liabilities"])
        if current_assets is None or current_liabilities is None:
            return None
        return current_assets / current_liabilities

    def calculate_pe_to_growth(self):
        """Retrieve the PEG Ratio from the info dictionary."""
        return self.info.get("pegRatio", None)

    def calculate_price_to_book(self):
        """Retrieve the Price-to-Book Ratio from the info dictionary."""
        return self.info.get("priceToBook", None)

    def calculate_price_to_sales(self):
        """Calculate the Price-to-Sales (P/S) ratio using Market Cap and Revenue."""
        market_cap = self.info.get("marketCap", None)
        revenue = self.get_revenue()
        if market_cap is None or revenue is None:
            return None
        return market_cap / revenue

    def calculate_ev_to_ebitda(self):
        """Calculate the EV/EBITDA ratio using Enterprise Value and EBITDA."""
        enterprise_value = self.info.get("enterpriseValue", None)
        ebitda = self._get_financials_value(["EBITDA"])
        if enterprise_value is None or ebitda is None:
            return None
        return enterprise_value / ebitda

    def calculate_free_cash_flow(self):
        """Calculate Free Cash Flow (Operating Cash Flow - Capital Expenditure)."""
        operating_cash_flow = self._get_cashflow_value(["Operating Cash Flow"])
        capital_expenditures = self._get_cashflow_value(["Capital Expenditure"])
        if operating_cash_flow is None or capital_expenditures is None:
            return None
        return operating_cash_flow - capital_expenditures

    def calculate_price_to_free_cash_flow(self):
        """Calculate Price-to-Free Cash Flow (P/FCF) ratio using Market Cap and Free Cash Flow."""
        market_cap = self.info.get("marketCap", None)
        free_cash_flow = self.calculate_free_cash_flow()
        if market_cap is None or free_cash_flow is None or free_cash_flow == 0:
            return None
        return market_cap / free_cash_flow

    def get_current_liabilities(self):
        """Retrieve Current Liabilities from the balance sheet."""
        return self._get_balance_sheet_value(["Current Liabilities"])

    def get_total_liabilities(self):
        """Retrieve Total Liabilities from the balance sheet."""
        return self._get_balance_sheet_value(
            ["Total Liabilities Net Minority Interest", "Total Liabilities"]
        )

    def get_current_assets(self):
        """Retrieve Current Assets from the balance sheet."""
        return self._get_balance_sheet_value(["Current Assets"])

    def get_total_stockholder_equity(self):
        """Retrieve Total Stockholder Equity from the balance sheet."""
        return self._get_balance_sheet_value(
            ["Common Stock Equity", "Stockholders Equity"]
        )

    def get_total_shares_outstanding(self):
        """Retrieve Total Shares Outstanding from the info dictionary."""
        shares_outstanding = self.info.get("sharesOutstanding", None)
        if shares_outstanding is not None:
            return f"{shares_outstanding:,.0f}"  # Format with commas and no decimals
        return None

    def get_book_value_of_equity(self):
        """
        Calculate the Book Value of Equity (Total Stockholder Equity / Total Shares Outstanding).
        """
        total_stockholder_equity = self.get_total_stockholder_equity()
        total_shares_outstanding = self.get_total_shares_outstanding()

        if total_stockholder_equity is None or total_shares_outstanding is None:
            return None

        # Ensure total_shares_outstanding is numeric
        total_shares = (
            float(total_shares_outstanding.replace(",", ""))
            if isinstance(total_shares_outstanding, str)
            else total_shares_outstanding
        )

        return total_stockholder_equity / total_shares if total_shares > 0 else None

    def calculate_book_value_per_share(self):
        """Calculate the Book Value Per Share."""
        stockholder_equity = self.get_total_stockholder_equity()
        shares_outstanding = self.get_total_shares_outstanding()
        if stockholder_equity is None or shares_outstanding is None:
            return None
        return stockholder_equity / float(shares_outstanding.replace(",", ""))

    def calculate_payout_ratio(self):
        """Retrieve the Payout Ratio from the info dictionary."""
        return self.info.get("payoutRatio", None)

    def get_beta(self):
        """Retrieve the Beta (Volatility) from the info dictionary."""
        return self.info.get("beta", None)

    def get_institutional_ownership(self):
        """Retrieve Institutional Ownership from the info dictionary."""
        return self.info.get("heldPercentInstitutions", None)

    def get_insider_transactions(self):
        """Retrieve Insider Buying/Selling percentage from the info dictionary."""
        return self.info.get("heldPercentInsiders", None)

    def calculate_asset_turnover_ratio(self):
        """Calculate the Asset Turnover Ratio using Total Assets and Revenue."""
        total_assets = self._get_balance_sheet_value(["Total Assets"])
        revenue = self.get_revenue()
        if total_assets is None or revenue is None:
            return None
        return revenue / total_assets

    def get_revenue(self):
        """Retrieve Total Revenue from the financials."""
        return self._get_financials_value(["Total Revenue"])

    def get_operating_income(self):
        """Retrieve Operating Income from the financials."""
        return self._get_financials_value(["Operating Income"])

    def get_interest_expense(self):
        """Retrieve Interest Expense from the financials."""
        return self._get_financials_value(["Interest Expense"])

    def get_rnd_expense(self):
        """Retrieve Research & Development Expense from the financials."""
        return self._get_financials_value(["Research Development"])

    def calculate_effective_tax_rate(self):
        """Calculate the Effective Tax Rate using Income Before Tax and Taxes Paid."""
        income_before_tax = self._get_financials_value(["Income Before Tax"])
        tax_paid = self._get_cashflow_value(["Tax Paid"])
        if income_before_tax is None or tax_paid is None:
            return None
        return tax_paid / income_before_tax
