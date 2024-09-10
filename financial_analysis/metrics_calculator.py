import pandas as pd

class MetricsCalculator:
    def __init__(self, balance_sheet: pd.DataFrame, financials: pd.DataFrame, cashflow: pd.DataFrame, info: dict):
        self.balance_sheet = balance_sheet
        self.financials = financials
        self.cashflow = cashflow
        self.info = info

    # Helper method to retrieve balance sheet values using multiple possible keys
    def _get_balance_sheet_value(self, keys):
        for key in keys:
            if key in self.balance_sheet.index:
                if not self.balance_sheet.loc[key].empty:
                    return self.balance_sheet.loc[key].iloc[0]
        return None

    # Helper method to retrieve financial values using multiple possible keys
    def _get_financials_value(self, keys):
        for key in keys:
            if key in self.financials.index:
                if not self.financials.loc[key].empty:
                    return self.financials.loc[key].iloc[0]
        return None

    def _get_cashflow_value(self, keys):
        for key in keys:
            if key in self.cashflow.index:
                if not self.cashflow.loc[key].empty:
                    return self.cashflow.loc[key].iloc[0]
        return None

    # Industry, Sector, Short Name retrieval
    def get_industry(self):
        return self.info.get('industry', None)

    def get_sector(self):
        return self.info.get('sector', None)

    def get_short_name(self):
        return self.info.get('shortName', None)

    # Stock Price, PE Ratio, EPS retrieval
    def get_stock_price(self):
        return self.info.get('currentPrice', None)

    def calculate_pe_ratio(self):
        return self.info.get('trailingPE', None)

    def get_eps(self):
        return self.info.get('trailingEps', None)

    # Debt-to-Equity Ratio (DE Ratio) using Total Liabilities and Common Stock Equity
    def calculate_de_ratio(self):
        total_liabilities = self._get_balance_sheet_value(['Total Liabilities Net Minority Interest', 'Total Liabilities'])
        total_stockholder_equity = self._get_balance_sheet_value(['Common Stock Equity', 'Stockholders Equity'])
        if total_liabilities is None or total_stockholder_equity is None:
            return None
        return total_liabilities / total_stockholder_equity

    # Return on Equity (ROE) using Net Income and Stockholder Equity
    def calculate_roe(self):
        net_income = self._get_financials_value(['Net Income'])
        total_stockholder_equity = self._get_balance_sheet_value(['Common Stock Equity', 'Stockholders Equity'])
        if net_income is None or total_stockholder_equity is None:
            return None
        return net_income / total_stockholder_equity

    # Earnings Yield = Net Income / Market Cap
    def calculate_earnings_yield(self):
        net_income = self._get_financials_value(['Net Income'])
        market_cap = self.info.get('marketCap', None)
        if net_income is None or market_cap is None:
            return None
        return net_income / market_cap

    # Dividend Yield from info
    def calculate_dividend_yield(self):
        return self.info.get('dividendYield', None)

    # Current Ratio using Total Current Assets and Total Current Liabilities
    def calculate_current_ratio(self):
        current_assets = self._get_balance_sheet_value(['Current Assets'])
        current_liabilities = self._get_balance_sheet_value(['Current Liabilities'])
        if current_assets is None or current_liabilities is None:
            return None
        return current_assets / current_liabilities

    # PE to Growth (PEG Ratio) from info
    def calculate_pe_to_growth(self):
        return self.info.get('pegRatio', None)

    # Price to Book Ratio from info
    def calculate_price_to_book(self):
        return self.info.get('priceToBook', None)

    # Price-to-Sales (P/S) ratio using Market Cap and Revenue
    def calculate_price_to_sales(self):
        market_cap = self.info.get('marketCap', None)
        revenue = self.get_revenue()
        if market_cap is None or revenue is None:
            return None
        return market_cap / revenue

    # EV/EBITDA ratio using Enterprise Value and EBITDA
    def calculate_ev_to_ebitda(self):
        enterprise_value = self.info.get('enterpriseValue', None)
        ebitda = self._get_financials_value(['EBITDA'])
        if enterprise_value is None or ebitda is None:
            return None
        return enterprise_value / ebitda

    # Calculate Free Cash Flow (FCF)
    def calculate_free_cash_flow(self):
        """Calculate Free Cash Flow (Operating Cash Flow - Capital Expenditure)."""
        operating_cash_flow = self._get_cashflow_value(['Operating Cash Flow'])
        capital_expenditures = self._get_cashflow_value(['Capital Expenditure'])

        if operating_cash_flow is None or capital_expenditures is None:
            return None
        return operating_cash_flow - capital_expenditures

    # Price to Free Cash Flow (P/FCF) using Market Cap and Free Cash Flow
    def calculate_price_to_free_cash_flow(self):
        """Calculate Price-to-Free Cash Flow (P/FCF) ratio."""
        market_cap = self.info.get('marketCap', None)
        free_cash_flow = self.calculate_free_cash_flow()

        if market_cap is None or free_cash_flow is None or free_cash_flow == 0:
            return None
        return market_cap / free_cash_flow

    # Current Liabilities retrieval
    def get_current_liabilities(self):
        return self._get_balance_sheet_value(['Current Liabilities'])

    # Total Liabilities retrieval
    def get_total_liabilities(self):
        return self._get_balance_sheet_value(['Total Liabilities Net Minority Interest', 'Total Liabilities'])

    # Current Assets retrieval
    def get_current_assets(self):
        return self._get_balance_sheet_value(['Current Assets'])

    # Total Stockholder Equity retrieval
    def get_total_stockholder_equity(self):
        return self._get_balance_sheet_value(['Common Stock Equity', 'Stockholders Equity'])

    # Total Shares Outstanding retrieval
    def get_total_shares_outstanding(self):
        shares_outstanding = self.info.get('sharesOutstanding', None)
        if shares_outstanding is not None:
            return f"{shares_outstanding:,.0f}"  # Format with commas and no decimals
        return None

    # Book Value Per Share calculation
    def calculate_book_value_per_share(self):
        stockholder_equity = self.get_total_stockholder_equity()
        shares_outstanding = self.get_total_shares_outstanding()
        if stockholder_equity is None or shares_outstanding is None:
            return None
        return stockholder_equity / float(shares_outstanding.replace(",", ""))

    # Payout Ratio retrieval
    def calculate_payout_ratio(self):
        return self.info.get('payoutRatio', None)

    # Beta (Volatility) retrieval
    def get_beta(self):
        return self.info.get('beta', None)

    # Institutional Ownership retrieval
    def get_institutional_ownership(self):
        return self.info.get('heldPercentInstitutions', None)

    # Insider Buying/Selling retrieval
    def get_insider_transactions(self):
        return self.info.get('heldPercentInsiders', None)

    # Asset Turnover Ratio calculation
    def calculate_asset_turnover_ratio(self):
        total_assets = self._get_balance_sheet_value(['Total Assets'])
        revenue = self.get_revenue()
        if total_assets is None or revenue is None:
            return None
        return revenue / total_assets

    # Retrieve total revenue
    def get_revenue(self):
        return self._get_financials_value(['Total Revenue'])

    # Retrieve operating income
    def get_operating_income(self):
        return self._get_financials_value(['Operating Income'])

    # Retrieve interest expense
    def get_interest_expense(self):
        return self._get_financials_value(['Interest Expense'])

    # Retrieve book value of equity
    def get_book_value_of_equity(self):
        return self._get_balance_sheet_value(['Common Stock Equity'])

    # Retrieve book value of debt
    def get_book_value_of_debt(self):
        return self._get_balance_sheet_value(['Total Debt'])

    # Retrieve cash and equivalents
    def get_cash(self):
        return self._get_balance_sheet_value(['Cash And Cash Equivalents'])

    # Retrieve short-term investments
    def get_short_term_investments(self):
        return self._get_balance_sheet_value(['Other Short Term Investments'])

    # Effective Tax Rate calculation
    def calculate_effective_tax_rate(self):
        income_before_tax = self._get_financials_value(['Income Before Tax'])
        tax_paid = self.cashflow.loc['Tax Paid'].iloc[0] if 'Tax Paid' in self.cashflow.index and not self.cashflow.loc['Tax Paid'].empty else None
        if income_before_tax is None or tax_paid is None:
            return None
        return tax_paid / income_before_tax

    # Retrieve R&D expense
    def get_rnd_expense(self):
        return self._get_financials_value(['Research Development'])
