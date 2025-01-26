from dataclasses import dataclass
from typing import Optional, List, Union, Dict, Any
import pandas as pd
from .utils import handle_api_errors


@dataclass
class FinancialData:
    balance_sheet: pd.DataFrame
    financials: pd.DataFrame
    cashflow: pd.DataFrame
    info: Dict[str, Any]


class MetricsCalculator:
    def __init__(
        self,
        balance_sheet: pd.DataFrame,
        financials: pd.DataFrame,
        cashflow: pd.DataFrame,
        info: dict,
    ) -> None:
        self.data = FinancialData(balance_sheet, financials, cashflow, info)

    def _get_value(
        self, source: pd.DataFrame, keys: List[str]
    ) -> Optional[Union[float, int]]:
        return next(
            (
                source.loc[key].iloc[0]
                for key in keys
                if key in source.index and not source.loc[key].empty
            ),
            None,
        )

    def _get_info_value(self, key: str) -> Optional[Union[float, int, str]]:
        return self.data.info.get(key)

    @handle_api_errors
    def _get_balance_sheet_value(self, keys: List[str]) -> Optional[float]:
        return self._get_value(self.data.balance_sheet, keys)

    @handle_api_errors
    def _get_financials_value(self, keys: List[str]) -> Optional[float]:
        return self._get_value(self.data.financials, keys)

    @handle_api_errors
    def _get_cashflow_value(self, keys: List[str]) -> Optional[float]:
        return self._get_value(self.data.cashflow, keys)

    # Basic Financial Data
    def get_industry(self) -> Optional[str]:
        return self._get_info_value("industry")

    def get_sector(self) -> Optional[str]:
        return self._get_info_value("sector")

    def get_short_name(self) -> Optional[str]:
        return self._get_info_value("shortName")

    def get_stock_price(self) -> Optional[float]:
        return self._get_info_value("currentPrice")

    @handle_api_errors
    def get_revenue(self) -> Optional[float]:
        return self._get_financials_value(["Total Revenue"])

    @handle_api_errors
    def get_operating_income(self) -> Optional[float]:
        return self._get_financials_value(["Operating Income"])

    @handle_api_errors
    def get_net_income(self) -> Optional[float]:
        return self._get_financials_value(["Net Income"])

    @handle_api_errors
    def get_total_assets(self) -> Optional[float]:
        return self._get_balance_sheet_value(["Total Assets"])

    @handle_api_errors
    def get_total_liabilities(self) -> Optional[float]:
        return self._get_balance_sheet_value(
            ["Total Liabilities Net Minority Interest", "Total Liabilities"]
        )

    @handle_api_errors
    def get_total_equity(self) -> Optional[float]:
        return self._get_balance_sheet_value(
            ["Common Stock Equity", "Stockholders Equity"]
        )

    @handle_api_errors
    def get_cogs(self) -> Optional[float]:
        return self._get_financials_value(["Cost Of Revenue"])

    @handle_api_errors
    def get_interest_expense(self) -> Optional[float]:
        return self._get_financials_value(["Interest Expense"])

    @handle_api_errors
    def get_operating_cash_flow(self) -> Optional[float]:
        return self._get_cashflow_value(["Operating Cash Flow"])

    @handle_api_errors
    def get_capital_expenditures(self) -> Optional[float]:
        return self._get_cashflow_value(["Capital Expenditure"])

    # Market Data
    def get_beta(self) -> Optional[float]:
        return self._get_info_value("beta")

    def get_institutional_ownership(self) -> Optional[float]:
        return self._get_info_value("heldPercentInstitutions")

    def get_insider_transactions(self) -> Optional[float]:
        return self._get_info_value("heldPercentInsiders")

    # Profitability Metrics
    @handle_api_errors
    def calculate_margin(
        self, numerator: Optional[float], denominator: Optional[float]
    ) -> Optional[float]:
        if not all([numerator is not None, denominator is not None, denominator != 0]):
            return None
        return numerator / denominator

    @handle_api_errors
    def calculate_gross_margin(self) -> Optional[float]:
        return self.calculate_margin(
            self.get_revenue() - self.get_cogs(), self.get_revenue()
        )

    @handle_api_errors
    def calculate_operating_margin(self) -> Optional[float]:
        return self.calculate_margin(self.get_operating_income(), self.get_revenue())

    @handle_api_errors
    def calculate_net_profit_margin(self) -> Optional[float]:
        return self.calculate_margin(self.get_net_income(), self.get_revenue())

    @handle_api_errors
    def calculate_roa(self) -> Optional[float]:
        return self.calculate_margin(self.get_net_income(), self.get_total_assets())

    @handle_api_errors
    def calculate_roe(self) -> Optional[float]:
        return self.calculate_margin(self.get_net_income(), self.get_total_equity())

    @handle_api_errors
    def calculate_roic(self) -> Optional[float]:
        operating_income = self.get_operating_income()
        total_equity = self.get_total_equity()
        total_debt = self.get_total_liabilities()

        if not all([operating_income, total_equity, total_debt]):
            return None

        tax_rate = self.calculate_effective_tax_rate() or 0.25
        nopat = operating_income * (1 - tax_rate)
        invested_capital = total_equity + total_debt

        return self.calculate_margin(nopat, invested_capital)

    # Leverage and Coverage Metrics
    @handle_api_errors
    def calculate_debt_to_equity(self) -> Optional[float]:
        return self.calculate_margin(
            self.get_total_liabilities(), self.get_total_equity()
        )

    @handle_api_errors
    def calculate_interest_coverage(self) -> Optional[float]:
        return self.calculate_margin(
            self.get_operating_income(), self.get_interest_expense()
        )

    # Market Metrics
    def calculate_pe_ratio(self) -> Optional[float]:
        return self._get_info_value("trailingPE")

    @handle_api_errors
    def calculate_peg_ratio(self) -> Optional[float]:
        return self.calculate_margin(
            self._get_info_value("trailingPE"),
            self._get_info_value("earningsQuarterlyGrowth"),
        )

    @handle_api_errors
    def calculate_price_to_sales(self) -> Optional[float]:
        return self.calculate_margin(
            self._get_info_value("marketCap"), self.get_revenue()
        )

    def calculate_price_to_book(self) -> Optional[float]:
        return self._get_info_value("priceToBook")

    @handle_api_errors
    def calculate_price_to_free_cash_flow(self) -> Optional[float]:
        return self.calculate_margin(
            self._get_info_value("marketCap"), self.calculate_free_cash_flow()
        )

    @handle_api_errors
    def calculate_ev_to_ebitda(self) -> Optional[float]:
        return self.calculate_margin(
            self._get_info_value("enterpriseValue"),
            self._get_financials_value(["EBITDA"]),
        )

    # Growth and Value Metrics
    @handle_api_errors
    def calculate_sustainable_growth_rate(self) -> Optional[float]:
        return self.calculate_margin(
            self.calculate_roe(),
            1 - self._get_info_value("payoutRatio"),
        )

    @handle_api_errors
    def calculate_altman_z_score(self) -> Optional[float]:
        total_assets = self.get_total_assets()
        if not total_assets:
            return None

        metrics = {
            "working_capital": self._get_balance_sheet_value(["Working Capital"]),
            "retained_earnings": self._get_balance_sheet_value(["Retained Earnings"]),
            "operating_income": self.get_operating_income(),
            "market_cap": self._get_info_value("marketCap"),
            "total_liabilities": self.get_total_liabilities(),
            "revenue": self.get_revenue(),
        }

        if not all(metrics.values()):
            return None

        coefficients = {
            "working_capital": 1.2,
            "retained_earnings": 1.4,
            "operating_income": 3.3,
            "market_cap": 0.6,
            "revenue": 1.0,
        }

        z_score = sum(
            coefficients[metric] * (value / total_assets)
            for metric, value in metrics.items()
            if metric != "total_liabilities"
        )
        z_score += (
            coefficients["market_cap"]
            * metrics["market_cap"]
            / metrics["total_liabilities"]
        )

        return z_score

    # Other Metrics
    def calculate_dividend_yield(self) -> Optional[float]:
        return self._get_info_value("dividendYield")

    def calculate_payout_ratio(self) -> Optional[float]:
        return self._get_info_value("payoutRatio")

    @handle_api_errors
    def calculate_asset_turnover_ratio(self) -> Optional[float]:
        return self.calculate_margin(self.get_revenue(), self.get_total_assets())

    @handle_api_errors
    def calculate_free_cash_flow(self) -> Optional[float]:
        operating_cash_flow = self.get_operating_cash_flow()
        capital_expenditures = self.get_capital_expenditures()

        if any(x is None for x in [operating_cash_flow, capital_expenditures]):
            return None

        return operating_cash_flow - capital_expenditures

    @handle_api_errors
    def calculate_effective_tax_rate(self) -> Optional[float]:
        return self.calculate_margin(
            self._get_cashflow_value(["Tax Paid"]),
            self._get_financials_value(["Income Before Tax"]),
        )
