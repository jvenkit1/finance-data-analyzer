import pandas as pd

class MetricsCalculator:
    def __init__(self, balance_sheet: pd.DataFrame, financials: pd.DataFrame, cashflow: pd.DataFrame, info: dict):
        self.balance_sheet = balance_sheet
        self.financials = financials
        self.cashflow = cashflow
        self.info = info

    def _get_balance_sheet_value(self, keys):
        """Helper function to get a value from the balance sheet, checking multiple possible keys."""
        for key in keys:
            if key in self.balance_sheet.index:
                if not self.balance_sheet.loc[key].empty:
                    return self.balance_sheet.loc[key].iloc[0]
        return None

    def _get_financials_value(self, keys):
        """Helper function to get a value from the financials, checking multiple possible keys."""
        for key in keys:
            if key in self.financials.index:
                if not self.financials.loc[key].empty:
                    return self.financials.loc[key].iloc[0]
        return None

    # First set of metrics
    def calculate_de_ratio(self):
        """Calculate Debt to Equity Ratio."""
        total_liabilities = self._get_balance_sheet_value(['Total Liabilities Net Minority Interest', 'Total Liab'])
        total_stockholder_equity = self._get_balance_sheet_value(['Common Stock Equity', 'Total Stockholder Equity'])

        if total_liabilities is None or total_stockholder_equity is None:
            return None
        return total_liabilities / total_stockholder_equity

    def calculate_roe(self):
        """Calculate Return on Equity."""
        net_income = self._get_financials_value(['Net Income'])
        total_stockholder_equity = self._get_balance_sheet_value(['Common Stock Equity', 'Total Stockholder Equity'])

        if net_income is None or total_stockholder_equity is None:
            return None
        return net_income / total_stockholder_equity

    def calculate_earnings_yield(self):
        """Calculate Earnings Yield = Net Income / Market Cap."""
        net_income = self._get_financials_value(['Net Income'])
        market_cap = self.info.get('marketCap', None)

        if net_income is None or market_cap is None:
            return None
        return net_income / market_cap

    def calculate_dividend_yield(self):
        """Calculate Dividend Yield."""
        return self.info.get('dividendYield', None)

    def calculate_current_ratio(self):
        """Calculate Current Ratio."""
        current_assets = self._get_balance_sheet_value(['Total Current Assets'])
        current_liabilities = self._get_balance_sheet_value(['Total Current Liabilities'])

        if current_assets is None or current_liabilities is None:
            return None
        return current_assets / current_liabilities

    def calculate_pe_to_growth(self):
        """Calculate Price/Earnings to Growth (PEG) ratio."""
        return self.info.get('pegRatio', None)

    def calculate_price_to_book(self):
        """Calculate Price to Book Ratio."""
        return self.info.get('priceToBook', None)

    def get_current_liabilities(self):
        """Retrieve current liabilities."""
        return self._get_balance_sheet_value(['Total Current Liabilities'])

    def get_current_assets(self):
        """Retrieve current assets."""
        return self._get_balance_sheet_value(['Total Current Assets'])

    def get_total_stockholder_equity(self):
        """Retrieve total stockholder equity."""
        return self._get_balance_sheet_value(['Common Stock Equity', 'Total Stockholder Equity'])

    def get_total_shares_outstanding(self):
        """Retrieve total shares outstanding and format it as a full number."""
        shares_outstanding = self.info.get('sharesOutstanding', None)
        if shares_outstanding is not None:
            return f"{shares_outstanding:,.0f}"  # Format with commas and no decimals
        return None

    def calculate_book_value_per_share(self):
        """Calculate Book Value per Share = Stockholder Equity / Shares Outstanding."""
        stockholder_equity = self.get_total_stockholder_equity()
        shares_outstanding = self.get_total_shares_outstanding()

        if stockholder_equity is None or shares_outstanding is None:
            return None
        return stockholder_equity / float(shares_outstanding.replace(",", ""))

    # Calculate Price-to-Sales (P/S) ratio
    def calculate_price_to_sales(self):
        """Calculate Price-to-Sales (P/S) ratio."""
        market_cap = self.info.get('marketCap', None)
        revenue = self.get_revenue()

        if market_cap is None or revenue is None:
            return None
        return market_cap / revenue

    # Calculate Enterprise Value to EBITDA (EV/EBITDA)
    def calculate_ev_to_ebitda(self):
        """Calculate Enterprise Value to EBITDA (EV/EBITDA)."""
        enterprise_value = self.info.get('enterpriseValue', None)
        ebitda = self._get_financials_value(['EBITDA'])

        if enterprise_value is None or ebitda is None:
            return None
        return enterprise_value / ebitda

    # Default set of metrics
    def get_short_name(self):
        """Retrieve company short name."""
        return self.info.get('shortName', None)

    def get_sector(self):
        """Retrieve company sector."""
        return self.info.get('sector', None)

    def get_industry(self):
        """Retrieve company industry."""
        return self.info.get('industry', None)

    def get_end_date(self):
        """Retrieve the most recent financial statement date."""
        return self.financials.columns[0] if not self.financials.empty else None

    def get_revenue(self):
        """Retrieve total revenue."""
        return self._get_financials_value(['Total Revenue'])

    def get_operating_income(self):
        """Retrieve operating income."""
        return self._get_financials_value(['Operating Income'])

    def get_interest_expense(self):
        """Retrieve interest expense."""
        return self._get_financials_value(['Interest Expense'])

    def get_book_value_of_equity(self):
        """Retrieve book value of equity."""
        return self._get_balance_sheet_value(['Common Stock Equity'])

    def get_book_value_of_debt(self):
        """Retrieve book value of debt."""
        return self._get_balance_sheet_value(['Total Debt'])

    def get_total_liabilities(self):
        """Retrieve total liabilities."""
        return self._get_balance_sheet_value(['Total Liabilities Net Minority Interest'])

    def get_cash(self):
        """Retrieve cash and equivalents."""
        return self._get_balance_sheet_value(['Cash And Cash Equivalents'])

    def get_short_term_investments(self):
        """Retrieve short-term investments."""
        return self._get_balance_sheet_value(['Other Short Term Investments'])

    def calculate_effective_tax_rate(self):
        """Calculate Effective Tax Rate."""
        income_before_tax = self._get_financials_value(['Income Before Tax'])
        tax_paid = self.cashflow.loc['Tax Paid'].iloc[0] if 'Tax Paid' in self.cashflow.index and not self.cashflow.loc['Tax Paid'].empty else None

        if income_before_tax is None or tax_paid is None:
            return None
        return tax_paid / income_before_tax

    def get_rnd_expense(self):
        """Retrieve R&D expense."""
        return self._get_financials_value(['Research Development'])
