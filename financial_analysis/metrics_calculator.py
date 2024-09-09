import pandas as pd

class MetricsCalculator:
    def __init__(self, balance_sheet: pd.DataFrame, financials: pd.DataFrame, cashflow: pd.DataFrame, info: dict, history: pd.DataFrame):
        self.balance_sheet = balance_sheet
        self.financials = financials
        self.cashflow = cashflow
        self.info = info
        self.history = history  # historical stock data for growth calculations

    def _get_balance_sheet_value(self, keys):
        """Helper function to retrieve values from the balance sheet."""
        for key in keys:
            if key in self.balance_sheet.index:
                if not self.balance_sheet.loc[key].empty:
                    return self.balance_sheet.loc[key].iloc[0]
        return None

    def _get_financials_value(self, keys):
        """Helper function to retrieve values from the financials."""
        for key in keys:
            if key in self.financials.index:
                if not self.financials.loc[key].empty:
                    return self.financials.loc[key].iloc[0]
        return None

    def safe_subtract(self, value1, value2):
        """Safely subtract two values, returns None if either is None."""
        if value1 is None or value2 is None:
            return None
        return value1 - value2

    def safe_divide(self, value1, value2):
        """Safely divides two values, returns None if either is None or divisor is zero."""
        if value1 is None or value2 is None or value2 == 0:
            return None
        return value1 / value2

    def get_revenue(self):
        """Retrieve total revenue."""
        return self._get_financials_value(['Total Revenue'])

    def get_gross_profit(self):
        """Retrieve gross profit."""
        return self._get_financials_value(['Gross Profit'])

    def get_operating_income(self):
        """Retrieve operating income."""
        return self._get_financials_value(['Operating Income', 'Total Operating Income As Reported'])

    def get_ebitda(self):
        """Retrieve EBITDA."""
        return self._get_financials_value(['EBITDA', 'Normalized EBITDA'])

    def get_ebit(self):
        """Retrieve EBIT."""
        return self._get_financials_value(['EBIT'])

    def get_net_income(self):
        """Retrieve net income."""
        return self._get_financials_value(['Net Income', 'Net Income Common Stockholders'])

    def get_free_cash_flow(self):
        """Retrieve free cash flow from the cash flow statement."""
        if 'Free Cash Flow' in self.cashflow.index:
            return self.cashflow.loc['Free Cash Flow'].iloc[0]
        return None

    def get_current_assets(self):
        """Retrieve current assets."""
        return self._get_balance_sheet_value(['Total Current Assets'])

    def get_current_liabilities(self):
        """Retrieve current liabilities."""
        return self._get_balance_sheet_value(['Total Current Liabilities'])

    def get_total_liabilities(self):
        """Retrieve total liabilities."""
        return self._get_balance_sheet_value(['Total Liabilities'])

    def get_stockholder_equity(self):
        """Retrieve stockholder equity."""
        return self._get_balance_sheet_value(['Stockholder Equity'])

    def calculate_revenue_growth(self, period='yoy'):
        """Calculate Revenue Growth YoY or QoQ."""
        revenue = self.get_revenue()
        revenue_history = self.history['Revenue'].dropna() if 'Revenue' in self.history.columns else []
        if len(revenue_history) < 5 or revenue is None:
            return None
        try:
            if period == 'yoy':
                return self.safe_divide(self.safe_subtract(revenue, revenue_history.iloc[-5]), revenue_history.iloc[-5])
            elif period == 'qoq':
                return self.safe_divide(self.safe_subtract(revenue, revenue_history.iloc[-1]), revenue_history.iloc[-1])
        except (TypeError, IndexError):
            return None
        return None

    def calculate_eps_growth(self, period='yoy'):
        """Calculate EPS Growth YoY or QoQ."""
        eps = self.info.get('trailingEps', None)
        eps_history = self.history['EPS'].dropna() if 'EPS' in self.history.columns else []
        if len(eps_history) < 5 or eps is None:
            return None
        try:
            if period == 'yoy':
                return self.safe_divide(self.safe_subtract(eps, eps_history.iloc[-5]), eps_history.iloc[-5])
            elif period == 'qoq':
                return self.safe_divide(self.safe_subtract(eps, eps_history.iloc[-1]), eps_history.iloc[-1])
        except (TypeError, IndexError):
            return None
        return None

    def calculate_fcf_growth(self, period='yoy'):
        """Calculate Free Cash Flow Growth YoY or QoQ."""
        fcf = self.get_free_cash_flow()
        fcf_history = self.history['Free Cash Flow'].dropna() if 'Free Cash Flow' in self.history.columns else []
        if len(fcf_history) < 5 or fcf is None:
            return None
        try:
            if period == 'yoy':
                return self.safe_divide(self.safe_subtract(fcf, fcf_history.iloc[-5]), fcf_history.iloc[-5])
            elif period == 'qoq':
                return self.safe_divide(self.safe_subtract(fcf, fcf_history.iloc[-1]), fcf_history.iloc[-1])
        except (TypeError, IndexError):
            return None
        return None

    def calculate_gross_profit_margin(self):
        """Calculate Gross Profit Margin."""
        revenue = self.get_revenue()
        gross_profit = self.get_gross_profit()
        return self.safe_divide(gross_profit, revenue)

    def calculate_operating_profit_margin(self):
        """Calculate Operating Profit Margin."""
        revenue = self.get_revenue()
        operating_income = self.get_operating_income()
        return self.safe_divide(operating_income, revenue)

    def calculate_net_profit_margin(self):
        """Calculate Net Profit Margin."""
        revenue = self.get_revenue()
        net_income = self.get_net_income()
        return self.safe_divide(net_income, revenue)

    def calculate_roic(self):
        """Calculate Return on Invested Capital (ROIC)."""
        net_income = self.get_net_income()
        total_capital = self.safe_subtract(self._get_balance_sheet_value(['Total Assets']), self._get_balance_sheet_value(['Total Current Liabilities']))
        return self.safe_divide(net_income, total_capital)

    def calculate_de_ratio(self):
        """Calculate Debt-to-Equity Ratio."""
        total_liabilities = self.get_total_liabilities()
        total_stockholder_equity = self.get_stockholder_equity()
        return self.safe_divide(total_liabilities, total_stockholder_equity)

    def calculate_current_ratio(self):
        """Calculate Current Ratio."""
        current_assets = self.get_current_assets()
        current_liabilities = self.get_current_liabilities()
        return self.safe_divide(current_assets, current_liabilities)

    def calculate_quick_ratio(self):
        """Calculate Quick Ratio (Current Ratio minus Inventory)."""
        current_assets = self.get_current_assets()
        inventory = self._get_balance_sheet_value(['Inventory'])
        current_liabilities = self.get_current_liabilities()
        return self.safe_divide(self.safe_subtract(current_assets, inventory), current_liabilities)

    def calculate_pfcf(self):
        """Calculate Price-to-Free Cash Flow (P/FCF)."""
        market_cap = self.info.get('marketCap', None)
        free_cash_flow = self.get_free_cash_flow()
        return self.safe_divide(market_cap, free_cash_flow)

    def calculate_peg_ratio(self):
        """Calculate PEG Ratio (P/E to Growth)."""
        return self.info.get('pegRatio', None)

    def calculate_dividend_yield(self):
        """Calculate Dividend Yield."""
        return self.info.get('dividendYield', None)

    def calculate_payout_ratio(self):
        """Calculate Dividend Payout Ratio."""
        return self.info.get('payoutRatio', None)

    def get_beta(self):
        """Retrieve Beta (Volatility)."""
        return self.info.get('beta', None)

    def get_institutional_ownership(self):
        """Retrieve Institutional Ownership."""
        return self.info.get('heldPercentInstitutions', None)

    def get_insider_transactions(self):
        """Retrieve Insider Buying/Selling Data."""
        return self.info.get('heldPercentInsiders', None)

    def calculate_asset_turnover_ratio(self):
        """Calculate Asset Turnover Ratio."""
        total_assets = self._get_balance_sheet_value(['Total Assets'])
        revenue = self.get_revenue()
        return self.safe_divide(revenue, total_assets)

    def get_industry(self):
        """Retrieve company industry."""
        return self.info.get('industry', None)

    def get_short_name(self):
        """Retrieve company short name."""
        return self.info.get('shortName', None)

    def get_sector(self):
        """Retrieve company sector."""
        return self.info.get('sector', None)

    def get_end_date(self):
        """Retrieve the most recent financial statement date."""
        return self.financials.columns[0] if not self.financials.empty else None
